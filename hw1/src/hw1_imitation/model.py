"""Model definitions for Push-T imitation policies."""

from __future__ import annotations

import abc
from typing import Literal, TypeAlias

import torch
import numpy as np
from torch import nn


class BasePolicy(nn.Module, metaclass=abc.ABCMeta):
    """Base class for action chunking policies."""

    def __init__(self, state_dim: int, action_dim: int, chunk_size: int) -> None:
        super().__init__()
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.chunk_size = chunk_size

    @abc.abstractmethod
    def compute_loss(
        self, state: torch.Tensor, action_chunk: torch.Tensor
    ) -> torch.Tensor:
        """Compute training loss for a batch."""

    @abc.abstractmethod
    def sample_actions(
        self,
        state: torch.Tensor,
        *,
        num_steps: int = 10,  # only applicable for flow policy
    ) -> torch.Tensor:
        """Generate a chunk of actions with shape (batch, chunk_size, action_dim)."""


class MSEPolicy(BasePolicy):
    """Predicts action chunks with an MSE loss."""

    ### TODO: IMPLEMENT MSEPolicy HERE ###
    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        chunk_size: int,
        hidden_dims: tuple[int, ...] = (128, 128),
    ) -> None:
        super().__init__(state_dim, action_dim, chunk_size)

        self.model = nn.Sequential(
          nn.Linear(state_dim, hidden_dims[0]),
          nn.ReLU(),
          nn.Linear(hidden_dims[0], hidden_dims[1]),
          nn.ReLU(),
          nn.Linear(hidden_dims[1], chunk_size * action_dim),
        )

    def compute_loss(
        self,
        state: torch.Tensor,
        action_chunk: torch.Tensor,
    ) -> torch.Tensor:
        pred = self.sample_actions(state)

        def loss(x, y):
            n, m, k = x.shape

            z = x - y
            z = z**2
            z = z.sum()
            z = z / (n * m * k)

            return z

        return loss(pred, action_chunk)

    def sample_actions(
        self,
        state: torch.Tensor,
        *,
        num_steps: int = 10,
    ) -> torch.Tensor:
        pred = self.model(state).reshape(-1, self.chunk_size, self.action_dim)
        return pred


class FlowMatchingPolicy(BasePolicy):
    """Predicts action chunks with a flow matching loss."""

    ### TODO: IMPLEMENT FlowMatchingPolicy HERE ###
    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        chunk_size: int,
        hidden_dims: tuple[int, ...] = (128, 128),
    ) -> None:
        super().__init__(state_dim, action_dim, chunk_size)

        # State + A + tau
        input_dim = state_dim + action_dim * chunk_size + 1

        self.model = nn.Sequential(
          nn.Linear(input_dim, hidden_dims[0]),
          nn.ReLU(),
          nn.Linear(hidden_dims[0], hidden_dims[1]),
          nn.ReLU(),
          nn.Linear(hidden_dims[1], chunk_size * action_dim),
        )

    def compute_loss(
        self,
        state: torch.Tensor,
        action_chunk: torch.Tensor,
    ) -> torch.Tensor:
        n, m, k = action_chunk.shape
        device = state.device

        a_0 = torch.randn(n, m * k).to(device)
        tau = torch.rand(n, 1).to(device)
        a_tau = tau * action_chunk.view(-1, m * k) + (1 - tau) * a_0
        a_sub = a_tau - a_0

        def loss(x, y):
            n, m = x.shape

            z = x - y
            z = z**2
            z = z.sum()
            z = z / (n * m)

            return z

        inp = torch.cat([state, a_tau, tau], dim=1)
        v = self.model(inp)

        return loss(v, a_sub)

    def sample_actions(
        self,
        state: torch.Tensor,
        *,
        num_steps: int = 10,
    ) -> torch.Tensor:
        n, m = state.shape
        device = state.device
        dtype = state.dtype

        a = torch.randn(n, self.chunk_size * self.action_dim).to(device)
        tau = torch.zeros(n, 1).to(device)

        for i in range(num_steps):
            inp = torch.cat([state, a, tau], dim=1)
            a = a + (1 / num_steps) * self.model(inp)
            tau += 1 / num_steps

        return a.reshape(-1, self.chunk_size, self.action_dim)

PolicyType: TypeAlias = Literal["mse", "flow"]


def build_policy(
    policy_type: PolicyType,
    *,
    state_dim: int,
    action_dim: int,
    chunk_size: int,
    hidden_dims: tuple[int, ...] = (128, 128),
) -> BasePolicy:
    if policy_type == "mse":
        return MSEPolicy(
            state_dim=state_dim,
            action_dim=action_dim,
            chunk_size=chunk_size,
            hidden_dims=hidden_dims,
        )
    if policy_type == "flow":
        return FlowMatchingPolicy(
            state_dim=state_dim,
            action_dim=action_dim,
            chunk_size=chunk_size,
            hidden_dims=hidden_dims,
        )
    raise ValueError(f"Unknown policy type: {policy_type}")

class FlowMatchingPolicy(BasePolicy):
    """Predicts action chunks with a flow matching loss."""

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        chunk_size: int,
        hidden_dims: tuple[int, ...] = (128, 128),
    ) -> None:
        super().__init__(state_dim, action_dim, chunk_size)

        # 입력: state_dim + (action_dim * chunk_size) + 1 (tau) 
        # 출력: action_dim * chunk_size (velocity) [cite: 52, 55]
        input_dim = state_dim + (action_dim * chunk_size) + 1
        output_dim = action_dim * chunk_size

        layers = []
        curr_dim = input_dim
        for h_dim in hidden_dims:
            layers.append(nn.Linear(curr_dim, h_dim))
            layers.append(nn.ReLU()) # 가이드라인 추천 [cite: 32, 65]
            curr_dim = h_dim
        layers.append(nn.Linear(curr_dim, output_dim))
        
        self.v_theta = nn.Sequential(*layers)

    def compute_loss(
        self,
        state: torch.Tensor,
        action_chunk: torch.Tensor,
    ) -> torch.Tensor:
        """Flow Matching Loss (Eq 2) [cite: 56]"""
        B = state.shape[0]
        device = state.device

        # 1. 샘플링: tau ~ U(0, 1), noise ~ N(0, I) [cite: 54, 55]
        tau = torch.rand((B, 1), device=device)
        noise = torch.randn_like(action_chunk)

        # 2. 보간 (Interpolation): A_tau = tau * A_target + (1 - tau) * A_0 [cite: 55]
        # (참고: 과제 문서 수식에 따라 구현)
        a_tau = tau * action_chunk + (1 - tau) * noise

        # 3. 모델 예측: v_theta(o_t, a_tau, tau) [cite: 55, 73]
        # 입력을 하나로 합쳐서 전달 (Batch, state + action_flat + 1)
        model_input = torch.cat([state, a_tau, tau], dim=-1)
        v_pred = self.v_theta(model_input)

        # 4. 정답 속도 (Target Velocity): A_target - A_0 [cite: 55, 56]
        v_target = action_chunk - noise

        # 5. MSE Loss 계산 [cite: 56]
        loss = torch.mean(torch.norm(v_pred - v_target, p=2, dim=-1)**2)
        return loss

    def sample_actions(
        self,
        state: torch.Tensor,
        *,
        num_steps: int = 10, # n (denoising steps) [cite: 61]
    ) -> torch.Tensor:
        """Inference using Euler integration (Eq 3) [cite: 58, 59]"""
        B = state.shape[0]
        device = state.device
        shape = (B, self.action_dim * self.chunk_size)

        # 1. 초기 노이즈 샘플링: A_t,0 ~ N(0, I) [cite: 58]
        a_tau = torch.randn(shape, device=device)
        dt = 1.0 / num_steps

        # 2. n번의 오일러 적분 수행 [cite: 59, 61]
        for i in range(num_steps):
            curr_tau = torch.full((B, 1), i * dt, device=device)
            
            model_input = torch.cat([state, a_tau, curr_tau], dim=-1)
            v_pred = self.v_theta(model_input)
            
            # A_{tau + 1/n} = A_tau + (1/n) * v_theta [cite: 59]
            a_tau = a_tau + dt * v_pred

        # 최종 결과 A_t,1을 반환 [cite: 61, 62]
        return a_tau

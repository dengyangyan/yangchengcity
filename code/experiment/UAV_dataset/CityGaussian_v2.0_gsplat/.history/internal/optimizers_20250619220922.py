from typing import Tuple
from dataclasses import dataclass
from typing import Any
import torch
from internal.configs.instantiate_config import InstantiatableConfig


@dataclass
class OptimizerConfig(InstantiatableConfig):
    def instantiate(self, params, lr: float, *args, **kwargs) -> Any:
        raise NotImplementedError()


@dataclass
class Adam(OptimizerConfig):
    def instantiate(self, params, lr: float, *args, **kwargs) -> Any:
        return torch.optim.Adam(
            params,
            lr,
            *args,
            **kwargs,
        )

@dataclass
class MUON(OptimizerConfig):
    def instantiate(self, params, lr: float, *args, **kwargs) -> Any:
        # optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, betas=(0.90, 0.95), weight_decay=0.01)

        # To replace the above, do the following:

        from muon import MuonWithAuxAdam
        # 如果 params 已经是参数组列表，直接使用
        if isinstance(params, list) and len(params) > 0 and isinstance(params[0], dict):
            # params 已经是参数组格式
            param_groups = []
            for group in params:
                new_group = group.copy()
                new_group.update({
                    'use_muon': True,
                    'lr': group.get('lr', lr),
                    'weight_decay': group.get('weight_decay', 0.01)
                })
                param_groups.append(new_group)
        else:
            # params 是单个参数列表或生成器
            param_groups = [
                dict(params=list(params), use_muon=True,
                    lr=lr, weight_decay=0.01),
            ]
        
        optimizer = MuonWithAuxAdam(param_groups)
        return optimizer



@dataclass
class SelectiveAdam(OptimizerConfig):
    betas: Tuple[float, float] = (0.9, 0.999)

    def instantiate(self, params, lr: float, *args, **kwargs) -> Any:
        for group in params:
            if "lr" not in group:
                group["lr"] = lr

        from gsplat.optimizers import SelectiveAdam
        from torch.optim.optimizer import _use_grad_for_differentiable

        class Adapter(SelectiveAdam):
            def on_after_backward(self, outputs, batch, gaussian_model, global_step, pl_module):
                self.visibility = outputs["viewspace_points"].has_hit_any_pixels

            @_use_grad_for_differentiable
            def step(self, closure=None):
                self._cuda_graph_capture_health_check()

                loss = None
                if closure is not None:
                    with torch.enable_grad():
                        loss = closure()

                super().step(self.visibility)

                return loss

        return Adapter(
            params,
            betas=self.betas,
            *args,
            **kwargs,
        )


@dataclass
class SparseGaussianAdam(OptimizerConfig):
    def instantiate(self, params, lr: float, *args, **kwargs) -> Any:
        from diff_accel_gaussian_rasterization import SparseGaussianAdam
        from torch.optim.optimizer import _use_grad_for_differentiable

        class Adapter(SparseGaussianAdam):
            def on_after_backward(self, outputs, batch, gaussian_model, global_step, pl_module):
                self.visibility = outputs["visibility_filter"]

            @_use_grad_for_differentiable
            def step(self, closure=None):
                self._cuda_graph_capture_health_check()

                loss = None
                if closure is not None:
                    with torch.enable_grad():
                        loss = closure()

                super().step(self.visibility, self.visibility.shape[0])

                return loss

        return Adapter(
            params,
            lr,
            *args,
            **kwargs,
        )

from omegaconf import DictConfig, OmegaConf, open_dict
from hydra import initialize, compose

def resolve_hydra_config(cfg: DictConfig) -> DictConfig:
    return OmegaConf.structured(OmegaConf.to_yaml(cfg, resolve=True))


def load_hydra_config(version_base='1.3', config_path=f"../../configs", config_name="server.yaml") -> open_dict:
    with initialize(version_base=version_base, config_path=config_path):
        hydra_cfg = compose(config_name=config_name)
    return hydra_cfg

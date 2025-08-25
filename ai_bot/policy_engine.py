from .utils import read_yaml
def load_policy(packs_dir: str, code: str):
    name = "federal" if code.upper()=="FED" else "state_x"
    return read_yaml(f"{packs_dir}/{name}.yaml")

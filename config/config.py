import yaml
from easydict import EasyDict


def read_yaml(file_path):
    with open(file_path, 'r') as file:
        cfg = yaml.safe_load(file)
    return EasyDict(cfg)


# 설정 파일 경로
yaml_file_path = r'../config/config.yaml'

# YAML 파일 읽기
config = read_yaml(yaml_file_path)
driver_path = config.paths.driver_path
chrome_path = config.paths.chrome_path

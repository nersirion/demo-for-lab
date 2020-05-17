import get_data


PATH = r"D:\For Wife\Source\test"


class Config:
    def __init__(self, path: str = PATH):
        config_path = f"{path}/config/config.xlsx"
        self.values_for_calculate = get_data.get_data_for_calculate(path)

    def __call__(self, sample: str) -> tuple:
        self.config = dict(self.values_for_calculate.loc[sample])
        self.config["sample"] = sample
        if "n_step" in self.config.keys():
            self.config["n_step"] = int(self.config["n_step"])

    def add_config(self, dict_to_excel: dict):
        self.config["n_cycles"] = len(dict_to_excel["Result"].columns)
        self.config["cycles"] = dict_to_excel["Result"].columns.astype(int)
        self.config["len_df"] = len(dict_to_excel["Voltage"])
        self.config["update_n_step"] = len(dict_to_excel["Result"].index) // 5



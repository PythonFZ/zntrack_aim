import zntrack
import numpy as np
import aim


def get_aim_run(node: zntrack.Node) -> aim.Run:
    uid = node.state.get_stage_hash()
    repo = aim.Repo(path=".")
    run_hash = None
    try:
        for run_metrics_col in repo.query_metrics(f"run.dvc_stage_hash == '{uid}'").iter():
            run_hash = run_metrics_col.run.hash
            break
    except:
        pass

    run = aim.Run(run_hash=run_hash)
    if run_hash is None:
        run["dvc_stage_hash"] = uid
    return run


class GenerateRandomNumbers(zntrack.Node):
    seed: int = zntrack.params()
    
    numbers: np.ndarray = zntrack.outs()

    def run(self):
        run = get_aim_run(self)

        rng = np.random.default_rng(self.seed)
        # generate 1000 random numbers
        self.numbers = rng.random(1000)
        run["mean"] = np.mean(self.numbers)
        run["std"] = np.std(self.numbers)

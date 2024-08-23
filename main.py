from src import GenerateRandomNumbers
import zntrack

with zntrack.Project() as proj:
    GenerateRandomNumbers(seed=42)

proj.build()

import jestspectation

# Use Jestspectation diffs for all objects
jestspectation.configure().pytest_all_diffs = True

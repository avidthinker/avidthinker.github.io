from scripts import run_generators, check_preview


def run_all(config):
    run_generators.run_generators(config)
    check_preview.check_preview(config)

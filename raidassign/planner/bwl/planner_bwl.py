from raidassign.planner.planner import BasePlanner


def get_3_tanks(tanks: list[str]) -> tuple[str, str, str]:
    """Extracts main tank and two offtanks from the list of tanks."""
    return tanks[0], tanks[1], tanks[2]


class PlannerBWL:
    @staticmethod
    def get_config(section: str) -> dict:
        # config = toml.load("mc_planner.toml")
        # return config[section]
        return {}

    @staticmethod
    def get_all() -> dict[str, BasePlanner]:
        from raidassign.planner.bwl.broodlord_lashlayer import BroodlordLashlayer
        from raidassign.planner.bwl.chromaggus import Chromaggus
        from raidassign.planner.bwl.ebonroc import Ebonroc
        from raidassign.planner.bwl.firemaw import Firemaw
        from raidassign.planner.bwl.flamegor import Flamegor
        from raidassign.planner.bwl.nefarian import Nefarian
        from raidassign.planner.bwl.razorgore import Razorgore
        from raidassign.planner.bwl.suppression_room import SuppressionRoom
        from raidassign.planner.bwl.vaelastrasz import Vaelastrasz
        return {
            "razorgore": Razorgore(),
            "vaelastrasz": Vaelastrasz(),
            "suppression": SuppressionRoom(),
            "broodlord": BroodlordLashlayer(),
            "firemaw": Firemaw(),
            "ebonroc": Ebonroc(),
            "flamegor": Flamegor(),
            "chromaggus": Chromaggus(),
            "nefarian": Nefarian(),
        }

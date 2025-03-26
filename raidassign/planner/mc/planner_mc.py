import toml
from raidassign.planner.mc.all_bosses_mc import AllBossesMC
from raidassign.planner.mc.garr import Garr
from raidassign.planner.mc.baron_geddon import BaronGeddon
from raidassign.planner.mc.gehennas import Gehennas
from raidassign.planner.mc.lucifron import Lucifron
from raidassign.planner.mc.magmadar import Magmadar
from raidassign.planner.mc.majordomo_executus import MajordomoExecutus
from raidassign.planner.mc.ragnaros import Ragnaros
from raidassign.planner.mc.shazzrah import Shazzrah
from raidassign.planner.mc.sulfuron_harbinger import SulfuronHarbinger
from raidassign.planner.planner import BasePlanner


class PlannerMC:
    @staticmethod
    def get_config(section: str) -> dict:
        config = toml.load("mc_planner.toml")
        return config[section]

    @staticmethod
    def get_3_tanks(tanks: list[str]) -> tuple[str, str, str]:
        """Extracts main tank and two offtanks from the list of tanks."""
        return tanks[0], tanks[1], tanks[2]

    @staticmethod
    def get_all() -> dict[str, BasePlanner]:
        return {
            "all": AllBossesMC(),
            "lucifron": Lucifron(),
            "magmadar": Magmadar(),
            "gehennas": Gehennas(),
            "garr": Garr(),
            "geddon": BaronGeddon(),
            "shazzrah": Shazzrah(),
            "sulfuron": SulfuronHarbinger(),
            "majordomo": MajordomoExecutus(),
            "ragnaros": Ragnaros()
        }

from raidassign.planpics.plan_painter import PlanPainter


plan = PlanPainter("images/bwl/room-razorgore.png")


def spawns(x: float, y: float, plan: PlanPainter):
    plan.add_icon("images/bwl/death-talon-dragonspawn.png",
                  (x, y), 64,
                  text="Dragonspawn", background_color=PlanPainter.COLOR_RAGE)
    plan.add_icon("images/bwl/blackwing-mage.png",
                  (x+0.1, y), 64,
                  text="Mage", background_color=PlanPainter.COLOR_MANA)
    plan.add_icon("images/bwl/blackwing-legionnaire.png",
                  (x+0.2, y), 64,
                  text="Legionnaire", background_color=PlanPainter.COLOR_RAGE)


spawns(0.10, 0.10, plan)
spawns(0.10, 0.90, plan)
spawns(0.70, 0.10, plan)
spawns(0.70, 0.90, plan)

plan.add_icon("images/bow-and-arrow.png",
              (0.5, 0.4), 96,
              text="Ranged And Healers",
              background_color=PlanPainter.COLOR_PLAYER)

plan.add_icon("images/shield.png",
              (0.5, 0.4), 96,
              text="Controller",
              background_color=PlanPainter.COLOR_PLAYER)


def players(x: float, y: float, group: str, plan: PlanPainter):
    plan.add_icon("images/orc.png",
                  (x, y), 64,
                  text=group,
                  background_color=PlanPainter.COLOR_PLAYER)


players(0.25, 0.25, "G1", plan)
players(0.1, 0.75, "G2", plan)
players(0.75, 0.25, "G3", plan)
players(0.9, 0.75, "G4", plan)

# Write io.BytesIO to a file
out_file = "test_image_plan_out.jpg"
with open(out_file, "wb") as f:
    f.write(plan.output(out_file).getbuffer())

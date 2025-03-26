from raidassign.planpics.plan_painter import PlanPainter


plan = PlanPainter("images/bwl/room-ebonroc-flamegor.png")

# Boss (black dragon)
plan.add_icon("images/black-dragon.png",
              (0.6, 0.3), 128,
              text="Ebonroc",
              background_color=PlanPainter.COLOR_RAGE)

# Tanks
plan.add_icon("images/shield.png",
              (0.65, 0.3), 48,
              text="Main Tank",
              background_color=PlanPainter.COLOR_PLAYER)
plan.add_icon("images/shield.png",
              (0.6, 0.2), 48,
              text="Offtank",
              background_color=PlanPainter.COLOR_PLAYER)

plan.add_icon("images/bow-and-arrow.png",
              (0.47, 0.63), 64,
              text="Ranged",
              background_color=PlanPainter.COLOR_PLAYER)
plan.add_icon("images/nurse.png",
              (0.43, 0.58), 64,
              text="Healers",
              background_color=PlanPainter.COLOR_PLAYER)

# Write io.BytesIO to a file
out_file = "test_image_plan_out.jpg"
with open(out_file, "wb") as f:
    f.write(plan.output(out_file).getbuffer())

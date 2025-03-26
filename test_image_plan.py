from raidassign.planpics.plan_painter import PlanPainter


plan = PlanPainter("images/bwl/room-chromaggus.png")

# Draw Red Zone where the boss will be casting the breaths
plan.draw_polygon(
    rel_points=[(0.0, 1.0), (0.0, 0.68), (0.33, 0.49), (0.37, 0.28), (0.46, 0.28), (0.47, 0.0),
                (0.65, 0.0), (0.625, 0.105), (0.64, 0.275), (0.725, 0.275), (0.78, 0.49), (1.0, 1.0)],
    color=(255, 0, 0, 64),
    outline=(255, 0, 0, 255),
    width=3)

# Boss (Cerberus icon)
plan.add_icon("images/bwl/cerberus.png",
              (0.55, 0.35), 160,
              text="Chromaggus",
              background_color=PlanPainter.COLOR_RAGE)

# Tanks
plan.add_icon("images/shield.png",
              (0.55, 0.53), 64,
              text="Main Tank",
              background_color=PlanPainter.COLOR_PLAYER)

for spot_rel in [(0.39, 0.25), (0.45, 0.175), (0.47, 0.05)]:
    plan.add_icon("images/orc.png",
                  spot_rel, 48,
                  text="Melee Safe Spot",
                  background_color=PlanPainter.COLOR_PLAYER)

plan.add_icon("images/bow-and-arrow.png",
              (0.15, 0.5), 64,
              text="Ranged",
              background_color=PlanPainter.COLOR_PLAYER)
plan.add_icon("images/nurse.png",
              (0.22, 0.5), 64,
              text="Healers",
              background_color=PlanPainter.COLOR_PLAYER)


# Write io.BytesIO to a file
out_file = "test_image_plan_out.jpg"
with open(out_file, "wb") as f:
    f.write(plan.output(out_file).getbuffer())

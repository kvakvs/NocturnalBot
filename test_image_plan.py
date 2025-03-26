from raidassign.planpics.plan_painter import PlanPainter


plan = PlanPainter("images/bwl/room-firemaw.png")
maintank_rel_xy = (0.8, 0.1)

# Draw the affected area from boss center to all edges of the doorway and safe spots
boss_rel_xy = (0.65, 0.37)
# Red AoE area going left
plan.draw_polygon(
    [boss_rel_xy, (0.33, 0.0), (0.0, 0.0), (0.0, 0.85)],
    color=(128, 0, 0, 64),
    outline=(255, 0, 0, 255),
    width=3)
# Red AoE area going right
plan.draw_polygon(
    [boss_rel_xy, (1.0, boss_rel_xy[1]), (1.0, 1.0), (0.47, 1.0)],
    color=(128, 0, 0, 64),
    outline=(255, 0, 0, 255),
    width=3)
# Green Maintank Healing Accessibility Zone
plan.draw_polygon(
    [maintank_rel_xy, (0.0, 0.38), (0.0, 1.0), (0.04, 1.0)],
    color=(0, 128, 0, 64),
    outline=(0, 255, 0, 255),
    width=2)

# Tanks
plan.add_icon("images/shield.png",
              maintank_rel_xy, 48,
              text="Main Tank",
              background_color=PlanPainter.COLOR_PLAYER)
plan.add_icon("images/shield.png",
              (0.45, 0.12), 48,
              text="Offtanks",
              background_color=PlanPainter.COLOR_PLAYER)

# Boss (black dragon)
plan.add_icon("images/black-dragon.png",
              boss_rel_xy, 200,
              text="Firemaw",
              background_color=PlanPainter.COLOR_RAGE)
# plan.add_circle((0.65, 0.25), 256, (255, 128, 0, 255), "Blast Wave 20 yd", width=2)

plan.add_icon("images/nurse.png",
              (0.2, 0.75), 64,
              text="MT Heal Safe Zone",
              background_color=PlanPainter.COLOR_PLAYER)

plan.add_icon("images/orc.png",
              (0.53, 0.75), 64,
              text="Melee Safe Zone",
              background_color=PlanPainter.COLOR_PLAYER)

plan.add_icon("images/bow-and-arrow.png",
              (0.4, 0.75), 64,
              text="Ranged Safe Zone",
              background_color=PlanPainter.COLOR_PLAYER)

# Write io.BytesIO to a file
out_file = "test_image_plan_out.jpg"
with open(out_file, "wb") as f:
    f.write(plan.output(out_file).getbuffer())

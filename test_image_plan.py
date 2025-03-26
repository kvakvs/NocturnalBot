from raidassign.planpics.plan_painter import PlanPainter


plan = PlanPainter("images/bwl/room-vaelastrasz.png")

plan.add_icon("images/bow-and-arrow.png",
              (0.8, 0.4), 96,
              text="Ranged And Healers",
              background_color=PlanPainter.COLOR_PLAYER)

plan.add_icon("images/orc.png",
              (0.4, 0.4), 64,
              text="Melee",
              background_color=PlanPainter.COLOR_PLAYER)

plan.add_icon("images/shield.png",
              (0.5, 0.2), 32,
              text="Main Tank",
              background_color=PlanPainter.COLOR_PLAYER)

plan.add_icon("images/red-dragon.png",
              (0.5, 0.4), 128,
              text="Vaelastrasz",
              background_color=PlanPainter.COLOR_RAGE)

plan.add_icon("images/bomb.png",
              (0.8, 0.9), 128,
              text="Bomb",
              background_color=PlanPainter.COLOR_PLAYER_ORANGE)

# Write io.BytesIO to a file
out_file = "test_image_plan_out.jpg"
with open(out_file, "wb") as f:
    f.write(plan.output(out_file).getbuffer())

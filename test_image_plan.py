from raidassign.planpics.plan_painter import PlanPainter


plan = PlanPainter("images/bwl/room-nefarian.png")

plan.add_icon("images/black-dragon.png",
              (0.45, 0.32), 200,
              text="Nefarian",
              background_color=PlanPainter.COLOR_RAGE)


plan.add_icon("images/bow-  Iand-arrow.png",
              (0.9, 0.4), 96,
              text="Ranged And Healers",
              background_color=PlanPainter.COLOR_PLAYER)

plan.add_icon("images/orc.png",
              (0.55, 0.3), 64,
              text="Melee",
              background_color=PlanPainter.COLOR_PLAYER)

plan.add_icon("images/shield.png",
              (0.45, 0.1), 32,
              text="Main Tank",
              background_color=PlanPainter.COLOR_PLAYER)

plan.add_icon("images/sheep.png",
              (0.7, 0.9), 80,
              text="Mage Call Safe Spot",
              background_color=PlanPainter.COLOR_PLAYER_ORANGE)
plan.draw_arrow((0.75, 0.87), 50, 270, color=(255, 255, 0, 255), width=3)

plan.draw_text((0.1, 0.05), "View of Searing Gorge", color=(255, 255, 0, 255))
plan.draw_arrow((0.17, 0.1), 50, 90, color=(255, 255, 0, 255), width=3)

plan.draw_text((0.93, 0.73), "Throne", color=(255, 255, 0, 255))

# Write io.BytesIO to a file
out_file = "test_image_plan_out.jpg"
with open(out_file, "wb") as f:
    f.write(plan.output(out_file).getbuffer())

from raidassign.planpics.plan_painter import PlanPainter


plan = PlanPainter("images/bwl/room-broodlord-lashlayer.png")

plan.add_icon("images/bow-and-arrow.png",
              (0.15, 0.25), 96,
              text="Ranged And Healers",
              background_color=PlanPainter.COLOR_PLAYER)

# A rogue guarding the traps
plan.add_icon("images/thief.png",
              (0.2, 0.5), 64,
              text="Rogue in Stealth",
              background_color=PlanPainter.COLOR_ENERGY)

# Tanks
plan.add_icon("images/shield.png",
              (0.65, 0.1), 32,
              text="Main Tank",
              background_color=PlanPainter.COLOR_PLAYER)
plan.add_icon("images/shield.png",
              (0.73, 0.15), 32,
              text="Offtank",
              background_color=PlanPainter.COLOR_PLAYER)

# Arrow from boss center for melee knockback direction
plan.draw_arrow((0.65, 0.25), length=250, angle_deg=180, color=(255, 128, 0, 255), width=3)
plan.draw_text((0.35, 0.25), "Safe Knockback Direction", color=(255, 128, 0, 255))
# Boss (strong)
plan.add_icon("images/bwl/icon-broodlord-strongman.png",
              (0.65, 0.25), 128,
              text="Broodlord Lashlayer",
              background_color=PlanPainter.COLOR_RAGE)
plan.add_circle((0.65, 0.25), 256, (255, 128, 0, 255), "Blast Wave 20 yd", width=2)

plan.add_icon("images/orc.png",
              (0.55, 0.25), 64,
              text="Melee",
              background_color=PlanPainter.COLOR_PLAYER)


# Write io.BytesIO to a file
out_file = "test_image_plan_out.jpg"
with open(out_file, "wb") as f:
    f.write(plan.output(out_file).getbuffer())

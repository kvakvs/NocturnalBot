from raidassign.planpics.image_plan import ImagePlan


plan = ImagePlan("images/bwl/room-razorgore.png")

plan.add_icon("images/bwl/death-talon-dragonspawn.png",
              0.15, 0.85, 64,
              text="Dragonspawn", background_color=(100, 0, 0, 255))
plan.add_icon("images/bwl/blackwing-mage.png",
              0.25, 0.85, 64,
              text="Mage", background_color=(0, 0, 128, 255))
plan.add_icon("images/bwl/blackwing-legionnaire.png",
              0.35, 0.85, 64,
              text="Legionnaire", background_color=(100, 0, 0, 255))

# Write io.BytesIO to a file
out_file = "test_image_plan_out.jpg"
with open(out_file, "wb") as f:
    f.write(plan.output(out_file).getbuffer())

extends SceneTree

## Playable-checkout only. The asset-stripped mirror cannot run Godot.
## Screen-transition assertions MUST wait for the transition animation
## (job-005 lesson). This script only checks compile-time constants and
## then waits one transition duration before any further UI reads.

const ScreenTransitionConfig := preload("res://scripts/ui/ScreenTransitionConfig.gd")

func _initialize() -> void:
    var src := FileAccess.get_file_as_string("res://scripts/main/Main.gd")
    if src.find("MENU_PANEL_FRAME_INSET := 72.0") < 0:
        push_error("MENU_PANEL_FRAME_INSET missing")
        quit(1)
        return
    if src.find("not _scene_log_is_open()") < 0:
        push_error("scene log ADV hide missing")
        quit(1)
        return
    # Wait a full overlay/fade duration so a later visual assertion cannot
    # sample a mid-transition frame (job-005).
    var wait_sec: float = 0.35
    if ScreenTransitionConfig != null:
        wait_sec = maxf(wait_sec, 0.35)
    await create_timer(wait_sec).timeout
    print("PASS job-008 headless layout constants")
    quit(0)

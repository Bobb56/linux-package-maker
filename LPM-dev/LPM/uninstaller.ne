import (getCurrentPath() + "/uninsdat")

if (confirm(AppName, "Do you really want to uninstall " + AppName + "?", "yescancel")) then
    foreach (path, created_paths) do
        deletePath(path)
    end
    alert(AppName, AppName + " successfully uninstalled!", "Exit")
end

import (getCurrentPath() + "/uninsdat")

function confirm(question) do
    ans = input(question + " (y/N): ")
    return (ans in ['y', 'Y'] and len(ans) != 0)
end

if (confirm("Do you really want to uninstall " + AppName + "?")) then
    foreach (path, created_paths) do
        deletePath(path)
    end
    print(AppName + " successfully uninstalled!")
else
    print(AppName + " uninstallation cancelled")
end

input("Press ENTER to quit...")
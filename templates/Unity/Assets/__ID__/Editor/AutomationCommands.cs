using System;
using System.IO;
using System.Linq;
using UnityEngine;

namespace __ID__.EditorTools
{
    /// <summary>
    /// Entry points for scripts and Claude. Run headless with
    /// Unity.exe -batchmode -nographics -quit -projectPath Unity -executeMethod __ID__.EditorTools.Automation.&lt;Method&gt;
    /// (the Editor must be closed for that project), or from the __NAME__ > Automation menu.
    /// Android builds are in AutomationAndroid.cs; tests, play mode and screenshots in Checks/Checks.cs.
    /// Add game-specific checks (for example a level validator) as more static methods here and
    /// name one in automation/config.json "contentCheckMethod" so the nightly job runs it.
    /// </summary>
    public static partial class Automation
    {
        static string ProjectRoot => Directory.GetParent(Application.dataPath).FullName;

        static bool HasArg(string name) => Environment.GetCommandLineArgs().Contains(name);

        static string ArgValue(string name)
        {
            var args = Environment.GetCommandLineArgs();
            int i = Array.IndexOf(args, name);
            return i >= 0 && i + 1 < args.Length ? args[i + 1] : null;
        }
    }
}

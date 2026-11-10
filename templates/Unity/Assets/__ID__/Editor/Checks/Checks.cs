using System;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEditor.TestTools.TestRunner.Api;
using UnityEngine;

namespace __ID__.EditorTools
{
    /// <summary>
    /// Checks Claude can run in the open Editor, through the Unity CLI
    /// (for example <c>unity command eval</c> calling <c>EditorApplication.ExecuteMenuItem</c>) or from the menu.
    /// Results go to automation/reports so a script or Claude can read them:
    /// tests_latest.json for tests, screenshots/ for play-mode captures.
    /// With the Editor closed, use automation/scripts/run_unity.ps1 -Method Tests instead.
    /// </summary>
    public static class Checks
    {
        const string Menu = "__NAME__/Automation/";

        [MenuItem(Menu + "Run Edit Mode Tests", priority = 70)]
        public static void RunEditModeTests()
        {
            var api = ScriptableObject.CreateInstance<TestRunnerApi>();
            api.RegisterCallbacks(new ResultWriter(api));
            api.Execute(new ExecutionSettings(new Filter { testMode = TestMode.EditMode }));
        }

        [MenuItem(Menu + "Enter Play Mode", priority = 71)]
        public static void Play() => EditorApplication.EnterPlaymode();

        [MenuItem(Menu + "Exit Play Mode", priority = 72)]
        public static void Stop() => EditorApplication.ExitPlaymode();

        /// <summary>Saves the Game view to automation/reports/screenshots. Only works in Play Mode; the file appears at the end of the frame.</summary>
        [MenuItem(Menu + "Take Screenshot", priority = 73)]
        public static void Screenshot() => Screenshot("check");

        public static string Screenshot(string name, int superSize = 1)
        {
            if (!EditorApplication.isPlaying)
            {
                Debug.LogWarning("__NAME__: enter Play Mode before taking a screenshot.");
                return null;
            }
            string dir = Path.Combine(ReportsDir, "screenshots");
            Directory.CreateDirectory(dir);
            string path = Path.Combine(dir, $"{name}_{DateTime.Now:yyyy-MM-dd_HHmmss}.png");
            ScreenCapture.CaptureScreenshot(path, superSize);
            Debug.Log($"__NAME__: screenshot -> {path}");
            return path;
        }

        static string ReportsDir => Path.GetFullPath(Path.Combine(Application.dataPath, "..", "..", "automation", "reports"));

        class ResultWriter : ICallbacks
        {
            readonly TestRunnerApi api;
            readonly List<string> failures = new List<string>();

            public ResultWriter(TestRunnerApi api) => this.api = api;

            public void RunStarted(ITestAdaptor testsToRun) { }

            public void TestStarted(ITestAdaptor test) { }

            public void TestFinished(ITestResultAdaptor result)
            {
                if (!result.HasChildren && result.TestStatus == TestStatus.Failed)
                    failures.Add($"{result.FullName}: {result.Message}");
            }

            public void RunFinished(ITestResultAdaptor result)
            {
                var summary = new TestSummary
                {
                    finished = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"),
                    passed = result.PassCount,
                    failed = result.FailCount,
                    skipped = result.SkipCount + result.InconclusiveCount,
                    failures = failures.ToArray(),
                };
                Directory.CreateDirectory(ReportsDir);
                string path = Path.Combine(ReportsDir, "tests_latest.json");
                File.WriteAllText(path, JsonUtility.ToJson(summary, true));
                Debug.Log($"__NAME__: tests {summary.passed} passed, {summary.failed} failed, {summary.skipped} skipped -> {path}");
                api.UnregisterCallbacks(this);
            }
        }

        [Serializable]
        class TestSummary
        {
            public string finished;
            public int passed, failed, skipped;
            public string[] failures;
        }
    }
}

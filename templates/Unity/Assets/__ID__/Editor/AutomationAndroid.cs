using System;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using UnityEngine;

namespace __ID__.EditorTools
{
    /// <summary>
    /// Android entry points: Player Settings from automation/config.json ("android" section),
    /// development APKs for the phone, and signed release bundles (.aab) for Google Play.
    /// Release signing reads the keystore from environment variables so no secret is saved in the project.
    /// </summary>
    public static partial class Automation
    {
        // Used for development APKs until android.packageId is set in automation/config.json.
        const string DevPackageId = "com.__LOWER__.dev";

        [Serializable]
        class AutomationConfig
        {
            public AndroidConfig android = new AndroidConfig();
        }

        [Serializable]
        class AndroidConfig
        {
            public string productName = "__NAME__";
            public string companyName = "";
            public string packageId = "";
            public string version = "0.1.0";
            public int versionCode = 1;
        }

        [MenuItem("__NAME__/Automation/Apply Android Player Settings", priority = 62)]
        public static void ApplyPlayerSettingsMenu()
        {
            string id = ApplyAndroidSettings(release: false);
            Debug.Log($"__NAME__: Player Settings applied ({PlayerSettings.productName}, {id}, portrait, IL2CPP ARM64).");
        }

        /// <summary>Applies the Android Player Settings from automation/config.json.</summary>
        public static void ApplyPlayerSettings()
        {
            bool ok = false;
            try { ApplyPlayerSettingsMenu(); ok = true; }
            catch (Exception e) { Debug.LogException(e); }
            if (Application.isBatchMode) EditorApplication.Exit(ok ? 0 : 1);
        }

        [MenuItem("__NAME__/Automation/Build Android APK", priority = 61)]
        public static void BuildAndroidMenu() => BuildAndroidInternal(ArtifactPath(".apk"), release: false);

        [MenuItem("__NAME__/Automation/Build Android Release (AAB)", priority = 63)]
        public static void BuildAndroidReleaseMenu() => BuildAndroidInternal(ArtifactPath(".aab"), release: true);

        /// <summary>Builds a development APK. Pass -buildPath to choose where it goes.</summary>
        public static void BuildAndroid() => RunBuild(release: false);

        /// <summary>Builds a signed release bundle (.aab) for Google Play. Pass -buildPath to choose where it goes.</summary>
        public static void BuildAndroidRelease() => RunBuild(release: true);

        static void RunBuild(bool release)
        {
            bool ok = false;
            try { ok = BuildAndroidInternal(ArgValue("-buildPath") ?? ArtifactPath(release ? ".aab" : ".apk"), release); }
            catch (Exception e) { Debug.LogException(e); }
            if (Application.isBatchMode) EditorApplication.Exit(ok ? 0 : 1);
        }

        static bool BuildAndroidInternal(string path, bool release)
        {
            EnsureGameScene();
            string id = ApplyAndroidSettings(release);
            bool signed = false;
            if (release && !(signed = UseReleaseKeystore())) return false;

            Directory.CreateDirectory(Path.GetDirectoryName(path));
            var scenes = EditorBuildSettings.scenes.Where(s => s.enabled).Select(s => s.path).ToArray();
            var options = new BuildPlayerOptions
            {
                scenes = scenes,
                locationPathName = path,
                target = BuildTarget.Android,
                targetGroup = BuildTargetGroup.Android,
                options = release ? BuildOptions.None : BuildOptions.Development,
            };
            try
            {
                EditorUserBuildSettings.buildAppBundle = release;
                var report = BuildPipeline.BuildPlayer(options);
                bool ok = report.summary.result == BuildResult.Succeeded;
                Debug.Log($"__NAME__: Android {(release ? "release" : "development")} build {report.summary.result}, " +
                          $"{report.summary.totalSize / (1024 * 1024)} MB, {report.summary.totalErrors} error(s), {id} -> {path}");
                return ok;
            }
            finally
            {
                EditorUserBuildSettings.buildAppBundle = false;
                if (signed)
                {
                    // Keep the keystore path and passwords out of ProjectSettings.asset.
                    PlayerSettings.Android.useCustomKeystore = false;
                    PlayerSettings.Android.keystoreName = "";
                    PlayerSettings.Android.keyaliasName = "";
                    AssetDatabase.SaveAssets();
                }
            }
        }

        /// <summary>Sets name, package id, version, portrait and what Google Play requires (IL2CPP, ARM64). Returns the package id.</summary>
        static string ApplyAndroidSettings(bool release)
        {
            var cfg = LoadAndroidConfig();
            string id = string.IsNullOrWhiteSpace(cfg.packageId) ? null : cfg.packageId.Trim();
            if (id == null)
            {
                if (release)
                    throw new InvalidOperationException("Set android.packageId in automation/config.json before a release build. It can't change after the first Play upload.");
                id = DevPackageId;
            }

            var android = NamedBuildTarget.Android;
            if (!string.IsNullOrWhiteSpace(cfg.productName)) PlayerSettings.productName = cfg.productName;
            if (!string.IsNullOrWhiteSpace(cfg.companyName)) PlayerSettings.companyName = cfg.companyName;
            PlayerSettings.SetApplicationIdentifier(android, id);
            if (!string.IsNullOrWhiteSpace(cfg.version)) PlayerSettings.bundleVersion = cfg.version;
            if (cfg.versionCode > 0) PlayerSettings.Android.bundleVersionCode = cfg.versionCode;
            PlayerSettings.defaultInterfaceOrientation = UIOrientation.Portrait;
            PlayerSettings.SetScriptingBackend(android, ScriptingImplementation.IL2CPP);
            PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARM64;
            AssetDatabase.SaveAssets();
            return id;
        }

        /// <summary>Reads __ENV___KEYSTORE, __ENV___KEYSTORE_PASS, __ENV___KEY_ALIAS and __ENV___KEY_PASS (defaults to the keystore password).</summary>
        static bool UseReleaseKeystore()
        {
            string store = Environment.GetEnvironmentVariable("__ENV___KEYSTORE");
            string storePass = Environment.GetEnvironmentVariable("__ENV___KEYSTORE_PASS");
            string alias = Environment.GetEnvironmentVariable("__ENV___KEY_ALIAS");
            string aliasPass = Environment.GetEnvironmentVariable("__ENV___KEY_PASS");
            if (string.IsNullOrEmpty(store) || !File.Exists(store) || string.IsNullOrEmpty(storePass) || string.IsNullOrEmpty(alias))
            {
                Debug.LogError("__NAME__: a release build needs __ENV___KEYSTORE (an existing file), __ENV___KEYSTORE_PASS and __ENV___KEY_ALIAS. See automation/README.md.");
                return false;
            }
            PlayerSettings.Android.useCustomKeystore = true;
            PlayerSettings.Android.keystoreName = store;
            PlayerSettings.Android.keystorePass = storePass;
            PlayerSettings.Android.keyaliasName = alias;
            PlayerSettings.Android.keyaliasPass = string.IsNullOrEmpty(aliasPass) ? storePass : aliasPass;
            return true;
        }

        static AndroidConfig LoadAndroidConfig()
        {
            string path = Path.Combine(ProjectRoot, "..", "automation", "config.json");
            if (!File.Exists(path)) return new AndroidConfig();
            return JsonUtility.FromJson<AutomationConfig>(File.ReadAllText(path))?.android ?? new AndroidConfig();
        }

        static void EnsureGameScene()
        {
            if (EditorBuildSettings.scenes.Any(s => s.enabled && File.Exists(s.path))) return;
            throw new InvalidOperationException("No enabled scene in Build Settings. Add the game scene under File > Build Profiles > Scene List, then build again.");
        }

        // Development APKs keep one name so install scripts find them; release bundles carry the version.
        static string ArtifactPath(string ext)
        {
            string name = ext == ".aab" ? $"__ID__-{LoadAndroidConfig().version}{ext}" : "__ID__" + ext;
            return Path.GetFullPath(Path.Combine(ProjectRoot, "..", "Builds", "Android", name));
        }
    }
}

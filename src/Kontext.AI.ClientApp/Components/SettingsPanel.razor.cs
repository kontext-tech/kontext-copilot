using System.Collections.Generic;
using Kontext.AI.ClientApp.Services;
using Microsoft.AspNetCore.Components;
using Microsoft.FluentUI.AspNetCore.Components;

namespace Kontext.AI.ClientApp.Components;

public partial class SettingsPanel
{
    private const string DefaultTheme = "Kontext-Next";
    private static readonly Dictionary<string, string> ThemeColors = new(){
        { "Kontext-Teal", "#008080" },
        { DefaultTheme, "#20c997" },
    };
    
    private static readonly string[] Colors = [.. ThemeColors.Values];
    private string? _status;
    private bool _ltr = true;
    private FluentDesignTheme? _theme;

    [Inject]
    public required ILogger<SettingsPanel> Logger { get; set; }

    [Inject]
    public required CacheStorageAccessor CacheStorageAccessor { get; set; }

    [Inject]
    public required GlobalState GlobalState { get; set; }

    public DesignThemeModes Mode { get; set; }

    public string? SelectedColor { get; set; }

    public LocalizationDirection? Direction { get; set; }

    private static IEnumerable<DesignThemeModes> AllModes => Enum.GetValues<DesignThemeModes>();

    protected override void OnAfterRender(bool firstRender)
    {
        if (firstRender)
        {
            Direction = GlobalState.Dir;
            _ltr = !Direction.HasValue || Direction.Value == LocalizationDirection.LeftToRight;
        }
    }

    private static string GetColorName(string? color)
    {
        return ThemeColors.FirstOrDefault(x => x.Value == color).Key;
    }

    protected void HandleDirectionChanged(bool isLeftToRight)
    {
        _ltr = isLeftToRight;
        Direction = isLeftToRight ? LocalizationDirection.LeftToRight : LocalizationDirection.RightToLeft;
    }

    private async Task ResetSiteAsync()
    {
        var msg = "Site settings reset and cache cleared!";

        await CacheStorageAccessor.RemoveAllAsync();
        _theme?.ClearLocalStorageAsync();

        Logger.LogInformation(msg);
        _status = msg;

        Mode = DesignThemeModes.System;
        SelectedColor = ThemeColors[DefaultTheme];
    }
}
using Microsoft.FluentUI.AspNetCore.Components;

namespace Kontext.AI.ClientApp.Components;

public partial class Settings
{
    private IDialogReference? _dialog;

    private async Task OpenSettingsAsync()
    {
        _dialog = await DialogService.ShowPanelAsync<SettingsPanel>(new DialogParameters()
        {
            ShowTitle = true,
            Title = "Site settings",
            Alignment = HorizontalAlignment.Right,
            PrimaryAction = "OK",
            SecondaryAction = null,
            ShowDismiss = true
        });

        DialogResult result = await _dialog.Result;
    }
}
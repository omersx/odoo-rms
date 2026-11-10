import { registry } from "@web/core/registry";
import { scanBarcode } from "@web/core/barcode/barcode_dialog";
import { isBarcodeScannerSupported } from "@web/core/barcode/barcode_video_scanner";
import { CharField, charField } from "@web/views/fields/char/char_field";

// One per page: browsers cap how many AudioContexts a page may create.
let audioContext = null;

// Chrome only lets audio start after a user gesture, so this is called from the click.
function ensureAudioContext() {
    if (!audioContext) {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        audioContext = AudioContext ? new AudioContext() : null;
    }
    return audioContext;
}

function beep() {
    const context = ensureAudioContext();
    if (!context) {
        return;
    }
    if (context.state === "suspended") {
        context.resume();
    }
    const oscillator = context.createOscillator();
    const gain = context.createGain();
    oscillator.type = "square";
    oscillator.frequency.value = 2200;
    gain.gain.setValueAtTime(0.12, context.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.0001, context.currentTime + 0.1);
    oscillator.connect(gain);
    gain.connect(context.destination);
    oscillator.start();
    oscillator.stop(context.currentTime + 0.1);
}

/**
 * Char field with a camera Scan button (same decoder as the POS / many2one fields).
 * Desktop included: core only shows its barcode button on mobile OSes.
 */
export class BarcodeScanField extends CharField {
    static template = "retail_management.BarcodeScanField";

    get canScan() {
        return !this.props.readonly && isBarcodeScannerSupported();
    }

    async onScanClick() {
        ensureAudioContext();
        const code = await scanBarcode(this.env);
        if (code) {
            beep();
            await this.props.record.update({ [this.props.name]: code });
        }
    }
}

registry.category("fields").add("barcode_scan", {
    ...charField,
    component: BarcodeScanField,
});

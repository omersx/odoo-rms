import { registry } from "@web/core/registry";
import { scanBarcode } from "@web/core/barcode/barcode_dialog";
import { isBarcodeScannerSupported } from "@web/core/barcode/barcode_video_scanner";
import { CharField, charField } from "@web/views/fields/char/char_field";

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
        const code = await scanBarcode(this.env);
        if (code) {
            await this.props.record.update({ [this.props.name]: code });
        }
    }
}

registry.category("fields").add("barcode_scan", {
    ...charField,
    component: BarcodeScanField,
});

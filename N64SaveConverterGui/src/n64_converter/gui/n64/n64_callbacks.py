# gui/n64/n64_callbacks.py

from systems.n64.n64_convert import convert_save

def convert_save_n64(input_path, source_var, source_type_var,
                     target_var, target_type_var, byteswap_var,
                     trim_pad_var, log_box):
    """
    Thin wrapper for GUI button. Pulls variables and passes to system convert.
    """
    convert_save(
        path=input_path.get(),
        src=source_var.get(),
        src_type=source_type_var.get(),
        tgt=target_var.get(),
        tgt_type=target_type_var.get(),
        byteswap_option=byteswap_var.get(),
        trim_pad_option=trim_pad_var.get(),
        log_box=log_box
    )

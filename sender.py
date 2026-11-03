def get_accounts():
    """Addresses from Calibre's 'Sharing books by email' settings, plus the default one."""
    from calibre.utils.smtp import config
    accts = config().parse().accounts  # {address: [formats, auto_send, is_default]}
    default = next((a for a, v in accts.items() if v[2]), None)
    return list(accts), default or next(iter(accts), None)

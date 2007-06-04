import logging
from ConfigParser import NoSectionError, NoOptionError

from gitosis import group

def haveAccess(config, user, mode, path):
    """
    Map request for write access to allowed path.

    Note for read-only access, the caller should check for write
    access too.

    Returns ``None`` for no access, or the physical repository path
    for access granted to that repository.
    """
    log = logging.getLogger('gitosis.access.haveAccess')

    log.debug(
        'Access check for %(user)r as %(mode)r on %(path)r...'
        % dict(
        user=user,
        mode=mode,
        path=path,
        ))

    for groupname in group.getMembership(config=config, user=user):
        try:
            repos = config.get('group %s' % groupname, mode)
        except (NoSectionError, NoOptionError):
            repos = []
        else:
            repos = repos.split()

        if path in repos:
            log.debug(
                'Access ok for %(user)r as %(mode)r on %(path)r'
                % dict(
                user=user,
                mode=mode,
                path=path,
                ))
            return path

        try:
            mapping = config.get('group %s' % groupname,
                                 'map %s %s' % (mode, path))
        except (NoSectionError, NoOptionError):
            pass
        else:
            log.debug(
                'Access ok for %(user)r as %(mode)r on %(path)r=%(mapping)r'
                % dict(
                user=user,
                mode=mode,
                path=path,
                mapping=mapping,
                ))
            return mapping
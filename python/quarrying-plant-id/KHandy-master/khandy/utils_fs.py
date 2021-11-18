import os
import re
import shutil


def get_path_stem(path):
    """
    References:
        `std::filesystem::path::stem` since C++17
    """
    return os.path.splitext(os.path.basename(path))[0]


def replace_path_stem(path, new_stem):
    dirname, basename = os.path.split(path)
    stem, extname = os.path.splitext(basename)
    if isinstance(new_stem, str):
        return os.path.join(dirname, new_stem + extname)
    elif hasattr(new_stem, '__call__'):
        return os.path.join(dirname, new_stem(stem) + extname)
    else:
        raise ValueError('Unsupported Type!')
        

def get_path_extension(path):
    """
    References:
        `std::filesystem::path::extension` since C++17
        
    Notes:
        Not fully consistent with `std::filesystem::path::extension`
    """
    return os.path.splitext(os.path.basename(path))[1]
    

def replace_path_extension(path, new_extname=None):
    """Replaces the extension with new_extname or removes it when the default value is used.
    Firstly, if this path has an extension, it is removed. Then, a dot character is appended 
    to the pathname, if new_extname is not empty or does not begin with a dot character.

    References:
        `std::filesystem::path::replace_extension` since C++17
    """
    filename_wo_ext = os.path.splitext(path)[0]
    if new_extname == '' or new_extname is None:
        return filename_wo_ext
    elif new_extname.startswith('.'):
        return ''.join([filename_wo_ext, new_extname]) 
    else:
        return '.'.join([filename_wo_ext, new_extname])


def makedirs(name, mode=0o755):
    """
    References:
        mmcv.mkdir_or_exist
    """
    if name == '':
        return
    name = os.path.expanduser(name)
    os.makedirs(name, mode=mode, exist_ok=True)


def listdirs(paths, path_sep=None, full_path=True):
    """Enhancement on `os.listdir`
    """
    assert isinstance(paths, (str, tuple, list))
    if isinstance(paths, str):
        path_sep = path_sep or os.path.pathsep
        paths = paths.split(path_sep)
        
    all_filenames = []
    for path in paths:
        path_ex = os.path.expanduser(path)
        filenames = os.listdir(path_ex)
        if full_path:
            filenames = [os.path.join(path_ex, filename) for filename in filenames]
        all_filenames.extend(filenames)
    return all_filenames


def _normalize_extensions(extensions):
    if extensions is None:
        return None
    new_extensions = []
    
    for extension in extensions:
        if extension.startswith('.'):
            new_extensions.append(extension.lower())
        else:
            new_extensions.append('.' + extension.lower())
    return new_extensions


def get_all_filenames(path, extensions=None, is_valid_file=None):
    if (extensions is not None) and (is_valid_file is not None):
        raise ValueError("Both extensions and is_valid_file cannot "
                         "be not None at the same time")
    if is_valid_file is None:
        if extensions is not None:
            if isinstance(extensions, str):
                extensions = [extensions]
            extensions = tuple(_normalize_extensions(extensions))
            def is_valid_file(filename):
                return filename.lower().endswith(extensions)
        else:
            def is_valid_file(filename):
                return True

    all_filenames = []
    path_ex = os.path.expanduser(path)
    for root, _, filenames in sorted(os.walk(path_ex, followlinks=True)):
        for filename in sorted(filenames):
            fullname = os.path.join(root, filename)
            if is_valid_file(fullname):
                all_filenames.append(fullname)
    return all_filenames


def get_top_level_dirs(path, full_path=True):
    if path is None:
        path = os.getcwd()
    path_ex = os.path.expanduser(path)
    filenames = os.listdir(path_ex)
    if full_path:
        return [os.path.join(path_ex, item) for item in filenames
                if os.path.isdir(os.path.join(path_ex, item))]
    else:
        return [item for item in filenames
                if os.path.isdir(os.path.join(path_ex, item))]


def get_top_level_files(path, full_path=True):
    if path is None:
        path = os.getcwd()
    path_ex = os.path.expanduser(path)
    filenames = os.listdir(path_ex)
    if full_path:
        return [os.path.join(path_ex, item) for item in filenames
                if os.path.isfile(os.path.join(path_ex, item))]
    else:
        return [item for item in filenames
                if os.path.isfile(os.path.join(path_ex, item))]
                

def replace_invalid_filename_char(filename, new_char='_'):
    assert isinstance(new_char, str)
    control_chars = ''.join((map(chr, range(0x00, 0x20))))
    pattern = r'[\\/*?:"<>|{}]'.format(control_chars)
    return re.sub(pattern, new_char, filename)


def copy_file(src, dst_dir, action_if_exist='rename'):
    """
    Args:
        src: source file path
        dst_dir: dest dir
        action_if_exist: 
            None: same as shutil.copy
            rename: when dest file exists, rename it
            
    Returns:
        dest filename
    """
    src_basename = os.path.basename(src)
    src_stem, src_extname = os.path.splitext(src_basename)
    dst = os.path.join(dst_dir, src_basename)
    
    if action_if_exist is None:
        os.makedirs(dst_dir, exist_ok=True)
        shutil.copy(src, dst_dir)
    elif action_if_exist.lower() == 'rename':
        suffix = 2
        while os.path.exists(dst):
            dst_basename = '{} ({}){}'.format(src_stem, suffix, src_extname)
            dst = os.path.join(dst_dir, dst_basename)
            suffix += 1
        else:
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy(src, dst)
    else:
        raise ValueError('Invalid action_if_exist, got {}.'.format(action_if_exist))
        
    return dst
    
    
def move_file(src, dst_dir, action_if_exist='rename'):
    """
    Args:
        src: source file path
        dst_dir: dest dir
        action_if_exist: 
            None: same as shutil.move
            rename: when dest file exists, rename it
            
    Returns:
        dest filename
    """
    src_basename = os.path.basename(src)
    src_stem, src_extname = os.path.splitext(src_basename)
    dst = os.path.join(dst_dir, src_basename)
    
    if action_if_exist is None:
        os.makedirs(dst_dir, exist_ok=True)
        shutil.move(src, dst_dir)
    elif action_if_exist.lower() == 'rename':
        suffix = 2
        while os.path.exists(dst):
            dst_basename = '{} ({}){}'.format(src_stem, suffix, src_extname)
            dst = os.path.join(dst_dir, dst_basename)
            suffix += 1
        else:
            os.makedirs(dst_dir, exist_ok=True)
            shutil.move(src, dst)
    else:
        raise ValueError('Invalid action_if_exist, got {}.'.format(action_if_exist))
        
    return dst
    
    
def rename_file(src, dst, action_if_exist='rename'):
    """
    Args:
        src: source file path
        dst: dest file path
        action_if_exist: 
            None: same as os.rename
            rename: when dest file exists, rename it
            
    Returns:
        dest filename
    """
    if dst == src:
        return dst
        
    if action_if_exist is None:
        os.rename(src, dst)
    elif action_if_exist.lower() == 'rename':
        dirname, basename = os.path.split(dst)
        stem, extname = os.path.splitext(basename)
        suffix = 2
        while os.path.exists(dst):
            new_basename = '{} ({}){}'.format(stem, suffix, extname)
            dst = os.path.join(dirname, new_basename)
            suffix += 1
        os.makedirs(dirname, exist_ok=True)
        os.rename(src, dst)
    else:
        raise ValueError('Invalid action_if_exist, got {}.'.format(action_if_exist))
        
    return dst
    
    
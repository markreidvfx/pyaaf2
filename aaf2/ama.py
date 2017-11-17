
from uuid import UUID


MediaContainerGUIDs = {
"Generic"        : (UUID("b22697a2-3442-44e8-bb8f-7a1cd290ebf1"),
    ('.3g2',   '.3gp',  '.aac', '.au',  '.avi', '.bmp', '.dv', '.gif',
     '.jfif',  '.jpeg', '.jpg', '.m4a', '.mid', '.moov', '.mov',
     '.movie', '.mp2',  '.mp3', '.mp4', '.mpa', '.mpe', '.mpeg',
     '.mpg',   '.png',  '.psd', '.qt',  '.tif', '.tiff',)),
"AVCHD"          : (UUID("f37d624b307d4ef59bebc539046cad54"),
    ('.mts', '.m2ts',)),
"ImageSequencer" : (UUID("4964178d-b3d5-485f-8e98-beb89d92a5f4"),
    ('.dpx',)),
"CanonRaw"       : (UUID("0f299461-ee19-459f-8ae6-93e65c76a892"),
    ('.rmf',)),
"WaveAiff"       : (UUID("3711d3cc-62d0-49d7-b0ae-c118101d1a16"),
    ('.wav', '.wave', '.bwf', '.aif', '.aiff', '.aifc', '.cdda',)),
"MXF"            : (UUID("60eb8921-2a02-4406-891c-d9b6a6ae0645"),
    ('.mxf',)),
"QuickTime"      : (UUID("781f84b7-b989-4534-8a07-c595cb9a6fb8"),
    ('.mov',  '.mp4',  '.m4v',   '.mpg',  '.mpe', '.mpeg', '.3gp', '.3g2',
     '.qt',   '.moov', '.movie', '.avi',  '.mp2', '.mp3',  '.m4a', '.wav',
     '.aiff', '.aif',  '.au',    '.aac',  '.mid', '.mpa',  '.gif', '.jpg',
     '.jpeg', '.jfif', '.tif',   '.tiff', '.png', '.bmp',  '.psd', '.dv')),
}

def create_ama_link(f, path, metadata, container="Generic"):
    pass

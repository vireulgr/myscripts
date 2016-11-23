#
#
#

# include functions
. "F:\prog\posh\functions.ps1"

# $md5Scr = 'f:\prog\posh\md5_files\md5_file.ps1'

[string[]]$fileList = `
    'G:\AnalysisTools\bash\analyzeAll\cores\trigger_012_HU_20160619_134355_SYS_CWD.tgz.dir\intel\Prediction.core',
     'G:\AnalysisTools\bash\analyzeAll\cores\trigger_011_HU_20160619_131808_SYS_CWD.tgz.dir\intel\Prediction.core';
#     'G:\AnalysisTools\perl\icb\workdir\ScpCtrl_FU.core',`
#     'G:\AnalysisTools\bash\analyzeAll\cores\trigger_029_FU_(000_HU)_20160613_141303_SYS_C.tgz.dir\intel\ScpCtrl_FU.core',`
#     'G:\AnalysisTools\bash\analyzeAll\cores\trigger_027_FU_(000_HU)_20160613_090041_SYS_C.tgz.dir\intel\ScpCtrl_FU.core';
     
     
     

#    '//OEFIW3FS05.hbi.ad.harman.com/Archivetraces/Dc/Ntg5/stability/2016/CW24/20160613_BB_BI_1483_BPfaendler_M067_C2_E230.504_16235AC2_Driving_Test.7z'

#   'F:\P4\p4_client_dev\tcfg\ntg5\9083_B1\arm\fs\ifs\boot\overrides\boot\lib\libmountObserve.so',`
#   'F:\P4\p4_client_e228\tcfg\ntg5\9083_B1\arm\fs\ifs\boot\overrides\boot\lib\libmountObserve.so',`
#   'F:\P4\p4_client_w205_rel5\tcfg\ntg5\9083_B1\arm\fs\ifs\boot\overrides\boot\lib\libmountObserve.so';


#   'C:/QNX650/target/qnx6/armle-v7/lib/libsocket.so.3',`
#   'F:\P4\p4_client_dev\deliveries\packages\sys-qnx-650sp1-all\bin\sys\qnx\target\qnx6\armle-v7\lib\libsocket.so.3';

foreach ( $file in $fileList ) {

    write $file
    write "size:", $(get-item $file).length
 #   & $md5Scr $file
    MD5File $file
}


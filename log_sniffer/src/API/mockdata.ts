import Log, { OS, Type } from "../models/Log";


export const mockedLogs: Log[] = [
    {
        id: "afdjioeaurf",
        type: Type.APP,
        os: OS.WINDOWS,
        hostname: "szymon-latitude",
        unit: "discrod.discord.process",
        message: "pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)",
        raw: "kwi 21 19:55:01 szymon-latitude CRON[8419]: pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)",
        severity: 0,
        timestamp: 1682100555.651589905
    },{
        id: "oweijr93847fh",
        type: Type.SYSTEM,
        os: OS.LINUX,
        hostname: "szymon-latitude",
        unit: "discrod.discord.process",
        message: "Run anacron jobs was skipped because of a failed condition check (ConditionACPower=true).",
        raw: "kwi 21 19:55:01 szymon-latitude CRON[8419]: pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)",
        severity: 1,
        timestamp: 1682130555.651589905
    },{
        id: "2938rujf948j",
        type: Type.APP,
        os: OS.LINUX,
        hostname: "szymon-latitude",
        unit: "discrod.discord.process.asfergstrgr.sdfhgyth.dsfgbythnrtfuydgb",
        message: "pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)",
        raw: "{\"_AUDIT_LOGINUID\":\"0\",\"_SYSTEMD_INVOCATION_ID\":\"2b6397718e6e4fdb96bacc3b515ce25a\",\"_EXE\":\"/usr/sbin/cron\",\"_SOURCE_REALTIME_TIMESTAMP\":\"1682102101662773\",\"_CMDLINE\":\"/usr/sbin/CRON -f -P\",\"_HOSTnameNAME\":\"szymon-latitude\",\"SYSLOG_FACILITY\":\"10\",\"_SELINUX_CONTEXT\":\"unconfined\",\"SYSLOG_PID\":\"9673\",\"_COMM\":\"cron\",\"SYSLOG_IDENTIFIER\":\"CRON\",\"_CAP_EFFECTIVE\":\"1ffffffffff\",\"SYSLOG_TIMESTAMP\":\"Apr 21 20:35:01 \",\"_AUDIT_SESSION\":\"18\",\"__REALTIME_TIMESTAMP\":\"1682102101662847\",\"_SYSTEMD_UNIT\":\"cron.service\",\"_UID\":\"0\",\"_SYSTEMD_SLICE\":\"system.slice\",\"__MONOTONIC_TIMESTAMP\":\"6129135497\",\"_PID\":\"9673\",\"MESSAGE\":\"pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)\",\"_TRANSPORT\":\"syslog\",\"PRIORITY\":\"6\",\"_MACHINE_ID\":\"c2a3a5aba18f4fbe97df329389ea3df0\",\"_GID\":\"0\",\"_SYSTEMD_CGROUP\":\"/system.slice/cron.service\",\"__CURSOR\":\"s=7731b3d110c143b5bc6aa2e3c227b048;i=c01811;b=e875e5d0d9a9455e88456c6109ae0133;m=16d532f89;t=5f9dcea3edc7f;x=d07b63559e112380\",\"_BOOT_ID\":\"e875e5d0d9a9455e88456c6109ae0133\"}",
        severity: 2,
        timestamp: 1682170555.651589905
    },{
        id: "2398rj3489fj",
        type: Type.SYSTEM,
        os: OS.WINDOWS,
        hostname: "szymon-latitude",
        unit: "discrod.discord.process",
        message: "pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)",
        raw: "{\"_AUDIT_LOGINUID\":\"0\",\"_SYSTEMD_INVOCATION_ID\":\"2b6397718e6e4fdb96bacc3b515ce25a\",\"_EXE\":\"/usr/sbin/cron\",\"_SOURCE_REALTIME_TIMESTAMP\":\"1682102101662773\",\"_CMDLINE\":\"/usr/sbin/CRON -f -P\",\"_HOSTnameNAME\":\"szymon-latitude\",\"SYSLOG_FACILITY\":\"10\",\"_SELINUX_CONTEXT\":\"unconfined\",\"SYSLOG_PID\":\"9673\",\"_COMM\":\"cron\",\"SYSLOG_IDENTIFIER\":\"CRON\",\"_CAP_EFFECTIVE\":\"1ffffffffff\",\"SYSLOG_TIMESTAMP\":\"Apr 21 20:35:01 \",\"_AUDIT_SESSION\":\"18\",\"__REALTIME_TIMESTAMP\":\"1682102101662847\",\"_SYSTEMD_UNIT\":\"cron.service\",\"_UID\":\"0\",\"_SYSTEMD_SLICE\":\"system.slice\",\"__MONOTONIC_TIMESTAMP\":\"6129135497\",\"_PID\":\"9673\",\"MESSAGE\":\"pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)\",\"_TRANSPORT\":\"syslog\",\"PRIORITY\":\"6\",\"_MACHINE_ID\":\"c2a3a5aba18f4fbe97df329389ea3df0\",\"_GID\":\"0\",\"_SYSTEMD_CGROUP\":\"/system.slice/cron.service\",\"__CURSOR\":\"s=7731b3d110c143b5bc6aa2e3c227b048;i=c01811;b=e875e5d0d9a9455e88456c6109ae0133;m=16d532f89;t=5f9dcea3edc7f;x=d07b63559e112380\",\"_BOOT_ID\":\"e875e5d0d9a9455e88456c6109ae0133\"}",
        severity: 3,
        timestamp: 1682202555.651589905
    },{
        id: "23k23ek230",
        type: Type.APP,
        os: OS.WINDOWS,
        hostname: "szymon-latitude",
        unit: "discrod.discord.process",
        message: "pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)",
        raw: "{\"_AUDIT_LOGINUID\":\"0\",\"_SYSTEMD_INVOCATION_ID\":\"2b6397718e6e4fdb96bacc3b515ce25a\",\"_EXE\":\"/usr/sbin/cron\",\"_SOURCE_REALTIME_TIMESTAMP\":\"1682102101662773\",\"_CMDLINE\":\"/usr/sbin/CRON -f -P\",\"_HOSTnameNAME\":\"szymon-latitude\",\"SYSLOG_FACILITY\":\"10\",\"_SELINUX_CONTEXT\":\"unconfined\",\"SYSLOG_PID\":\"9673\",\"_COMM\":\"cron\",\"SYSLOG_IDENTIFIER\":\"CRON\",\"_CAP_EFFECTIVE\":\"1ffffffffff\",\"SYSLOG_TIMESTAMP\":\"Apr 21 20:35:01 \",\"_AUDIT_SESSION\":\"18\",\"__REALTIME_TIMESTAMP\":\"1682102101662847\",\"_SYSTEMD_UNIT\":\"cron.service\",\"_UID\":\"0\",\"_SYSTEMD_SLICE\":\"system.slice\",\"__MONOTONIC_TIMESTAMP\":\"6129135497\",\"_PID\":\"9673\",\"MESSAGE\":\"pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)\",\"_TRANSPORT\":\"syslog\",\"PRIORITY\":\"6\",\"_MACHINE_ID\":\"c2a3a5aba18f4fbe97df329389ea3df0\",\"_GID\":\"0\",\"_SYSTEMD_CGROUP\":\"/system.slice/cron.service\",\"__CURSOR\":\"s=7731b3d110c143b5bc6aa2e3c227b048;i=c01811;b=e875e5d0d9a9455e88456c6109ae0133;m=16d532f89;t=5f9dcea3edc7f;x=d07b63559e112380\",\"_BOOT_ID\":\"e875e5d0d9a9455e88456c6109ae0133\"}",
        severity: 4,
        timestamp: 1682304555.651589905
    },{
        id: "cjniwefffe7",
        type: Type.APP,
        os: OS.WINDOWS,
        hostname: "szymon-latitude",
        unit: "discrod.discord.process",
        message: "pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)",
        raw: "{\"_AUDIT_LOGINUID\":\"0\",\"_SYSTEMD_INVOCATION_ID\":\"2b6397718e6e4fdb96bacc3b515ce25a\",\"_EXE\":\"/usr/sbin/cron\",\"_SOURCE_REALTIME_TIMESTAMP\":\"1682102101662773\",\"_CMDLINE\":\"/usr/sbin/CRON -f -P\",\"_HOSTnameNAME\":\"szymon-latitude\",\"SYSLOG_FACILITY\":\"10\",\"_SELINUX_CONTEXT\":\"unconfined\",\"SYSLOG_PID\":\"9673\",\"_COMM\":\"cron\",\"SYSLOG_IDENTIFIER\":\"CRON\",\"_CAP_EFFECTIVE\":\"1ffffffffff\",\"SYSLOG_TIMESTAMP\":\"Apr 21 20:35:01 \",\"_AUDIT_SESSION\":\"18\",\"__REALTIME_TIMESTAMP\":\"1682102101662847\",\"_SYSTEMD_UNIT\":\"cron.service\",\"_UID\":\"0\",\"_SYSTEMD_SLICE\":\"system.slice\",\"__MONOTONIC_TIMESTAMP\":\"6129135497\",\"_PID\":\"9673\",\"MESSAGE\":\"pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)\",\"_TRANSPORT\":\"syslog\",\"PRIORITY\":\"6\",\"_MACHINE_ID\":\"c2a3a5aba18f4fbe97df329389ea3df0\",\"_GID\":\"0\",\"_SYSTEMD_CGROUP\":\"/system.slice/cron.service\",\"__CURSOR\":\"s=7731b3d110c143b5bc6aa2e3c227b048;i=c01811;b=e875e5d0d9a9455e88456c6109ae0133;m=16d532f89;t=5f9dcea3edc7f;x=d07b63559e112380\",\"_BOOT_ID\":\"e875e5d0d9a9455e88456c6109ae0133\"}",
        severity: 5,
        timestamp: 1682326555.651589905
    },{
        id: "c342r24ffwe",
        type: Type.APP,
        os: OS.WINDOWS,
        hostname: "szymon-latitude",
        unit: "discrod.discord.process",
        message: "pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)",
        raw: "{\"_AUDIT_LOGINUID\":\"0\",\"_SYSTEMD_INVOCATION_ID\":\"2b6397718e6e4fdb96bacc3b515ce25a\",\"_EXE\":\"/usr/sbin/cron\",\"_SOURCE_REALTIME_TIMESTAMP\":\"1682102101662773\",\"_CMDLINE\":\"/usr/sbin/CRON -f -P\",\"_HOSTnameNAME\":\"szymon-latitude\",\"SYSLOG_FACILITY\":\"10\",\"_SELINUX_CONTEXT\":\"unconfined\",\"SYSLOG_PID\":\"9673\",\"_COMM\":\"cron\",\"SYSLOG_IDENTIFIER\":\"CRON\",\"_CAP_EFFECTIVE\":\"1ffffffffff\",\"SYSLOG_TIMESTAMP\":\"Apr 21 20:35:01 \",\"_AUDIT_SESSION\":\"18\",\"__REALTIME_TIMESTAMP\":\"1682102101662847\",\"_SYSTEMD_UNIT\":\"cron.service\",\"_UID\":\"0\",\"_SYSTEMD_SLICE\":\"system.slice\",\"__MONOTONIC_TIMESTAMP\":\"6129135497\",\"_PID\":\"9673\",\"MESSAGE\":\"pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)\",\"_TRANSPORT\":\"syslog\",\"PRIORITY\":\"6\",\"_MACHINE_ID\":\"c2a3a5aba18f4fbe97df329389ea3df0\",\"_GID\":\"0\",\"_SYSTEMD_CGROUP\":\"/system.slice/cron.service\",\"__CURSOR\":\"s=7731b3d110c143b5bc6aa2e3c227b048;i=c01811;b=e875e5d0d9a9455e88456c6109ae0133;m=16d532f89;t=5f9dcea3edc7f;x=d07b63559e112380\",\"_BOOT_ID\":\"e875e5d0d9a9455e88456c6109ae0133\"}",
        severity: 6,
        timestamp: 1682328555.651589905
    },{
        id: "cjnisuher8f7",
        type: Type.APP,
        os: OS.WINDOWS,
        hostname: "szymon-latitude",
        unit: "discrod.discord.process",
        message: "pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)",
        raw: "{\"_AUDIT_LOGINUID\":\"0\",\"_SYSTEMD_INVOCATION_ID\":\"2b6397718e6e4fdb96bacc3b515ce25a\",\"_EXE\":\"/usr/sbin/cron\",\"_SOURCE_REALTIME_TIMESTAMP\":\"1682102101662773\",\"_CMDLINE\":\"/usr/sbin/CRON -f -P\",\"_HOSTnameNAME\":\"szymon-latitude\",\"SYSLOG_FACILITY\":\"10\",\"_SELINUX_CONTEXT\":\"unconfined\",\"SYSLOG_PID\":\"9673\",\"_COMM\":\"cron\",\"SYSLOG_IDENTIFIER\":\"CRON\",\"_CAP_EFFECTIVE\":\"1ffffffffff\",\"SYSLOG_TIMESTAMP\":\"Apr 21 20:35:01 \",\"_AUDIT_SESSION\":\"18\",\"__REALTIME_TIMESTAMP\":\"1682102101662847\",\"_SYSTEMD_UNIT\":\"cron.service\",\"_UID\":\"0\",\"_SYSTEMD_SLICE\":\"system.slice\",\"__MONOTONIC_TIMESTAMP\":\"6129135497\",\"_PID\":\"9673\",\"MESSAGE\":\"pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)\",\"_TRANSPORT\":\"syslog\",\"PRIORITY\":\"6\",\"_MACHINE_ID\":\"c2a3a5aba18f4fbe97df329389ea3df0\",\"_GID\":\"0\",\"_SYSTEMD_CGROUP\":\"/system.slice/cron.service\",\"__CURSOR\":\"s=7731b3d110c143b5bc6aa2e3c227b048;i=c01811;b=e875e5d0d9a9455e88456c6109ae0133;m=16d532f89;t=5f9dcea3edc7f;x=d07b63559e112380\",\"_BOOT_ID\":\"e875e5d0d9a9455e88456c6109ae0133\"}",
        severity: 7,
        timestamp: 1682330555.651589905
    }
]
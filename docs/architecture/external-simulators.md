# Deterministic external simulator contracts

Future adapters may simulate IBM MQ, REST/HTTP, SFTP/FTP, Connect:Direct/NDM, SMTP, external databases, and other partners. A simulator is a test dependency—not evidence of the real product. Each versioned script captures requests, selects deterministic responses, supports explicit failure/latency/timeout injection, propagates correlation IDs, and replays from captured seed and virtual time. Scripts, requests, responses, and configuration are content-addressed artifacts. Full simulators are intentionally deferred.

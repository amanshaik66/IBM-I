**free
// UNVERIFIED ON IBM i — foundation fixture IBMSEM-RPG-WRITE-0001
ctl-opt option(*srcstmt);
dcl-f ACCTPF usage(*output);
write ACCTREC;
*inlr = *on;

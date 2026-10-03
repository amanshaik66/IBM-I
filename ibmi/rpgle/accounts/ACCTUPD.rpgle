**free
// UNVERIFIED ON IBM i — foundation fixture IBMSEM-RPG-UPDATE-0001
ctl-opt option(*srcstmt);
dcl-f ACCTPF keyed usage(*update);
update ACCTREC;
*inlr = *on;

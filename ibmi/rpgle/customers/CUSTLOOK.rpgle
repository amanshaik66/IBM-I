**free
// UNVERIFIED ON IBM i — CHAIN fixtures IBMSEM-RPG-CHAIN-0001/0002
ctl-opt option(*srcstmt);
dcl-f CUSTPF keyed usage(*input);
dcl-s RequestedId packed(9:0);
RequestedId = 1;
chain RequestedId CUSTREC;
*inlr = *on;

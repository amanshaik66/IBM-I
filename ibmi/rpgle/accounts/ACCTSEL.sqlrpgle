**free
// UNVERIFIED ON IBM i — foundation fixture IBMSEM-SQL-SELECT-0001
exec sql set option commit = *none;
dcl-s Balance packed(15:2);
exec sql select BALANCE into :Balance from ACCT where ACCTID = 1;
*inlr = *on;

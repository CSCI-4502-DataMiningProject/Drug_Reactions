create table indi (
primaryid varchar,
caseid varchar,
indi_drug_seq varchar,
indi_pt varchar);

create table outc (
primaryid varchar,
caseid varchar,
outc_cod varchar);

create table reac (
primaryid varchar,
caseid varchar,
pt varchar,
drug_rec_act varchar);

create table rpsr (
primaryid varchar,
caseid varchar,
rpsr_cod varchar);

create table ther (
primaryid varchar,
caseid varchar,
dsg_drug_seq varchar,
start_dt varchar,
start_dt_num varchar,
end_dt varchar,
end_dt_num varchar,
dur varchar,
dur_cod varchar);

create table demo (
primaryid varchar,
caseid varchar,
caseversion varchar,
i_f_code varchar,
i_f_code_num varchar,
event_dt varchar,
event_dt_num varchar,
mfr_dt varchar,
mfr_dt_num varchar,
init_fda_dt varchar,
init_fda_dt_num varchar,
fda_dt varchar,
fda_dt_num varchar,
rept_cod varchar,
rept_cod_num varchar,
auth_num varchar,
mfr_num varchar,
mfr_sndr varchar,
lit_ref varchar,
age varchar,
age_cod varchar,
age_grp varchar,
age_grp_num varchar,
sex varchar,
e_sub varchar,
wt varchar,
wt_cod varchar,
rept_dt varchar,
rept_dt_num varchar,
to_mfr varchar,
occp_cod varchar,
reporter_country varchar,
occr_country varchar,
occp_cod_num varchar);

create table drug (
primaryid varchar,
caseid varchar,
drug_seq varchar,
role_cod varchar,
drugname varchar,
prod_ai varchar,
val_vbm varchar,
route varchar,
dose_vbm varchar,
cum_dose_chr varchar,
cum_dose_unit varchar,
dechal varchar,
rechal varchar,
lot_num varchar,
exp_dt varchar,
exp_dtstr varchar,
exp_dt_mult varchar,
nda_num varchar,
dose_amt varchar,
dose_unit varchar,
dose_form varchar,
dose_freq varchar);

create or replace function init_table(varchar, int, int) returns void as
$$
declare
  low varchar := concat($2, 'days');
  up varchar := concat($3, 'days');
  query varchar := 'create temp table %s as
                    select conversions.user_id, sum(price*quantity) as %s
                    from conversions
                    join users
                    on conversions.user_id=users.user_id
                       and conversions.timestamp - users.signup_time >= %s
                       and conversions.timestamp - users.signup_time < %s
                    group by conversions.user_id;';
begin
   execute format(query, $1, $1, quote_literal(low),quote_literal(up));
end;
$$
language plpgsql;

create or replace function create_column(varchar) returns varchar as $$
declare
  query_create varchar := 'alter table days_revenues add column %s float;';
begin
  return format(query_create, $1);
end;
$$
language plpgsql;

create or replace function update_column(varchar) returns varchar as
$$
declare
  query varchar := 'update days_revenues set %s = %s.%s from %s where days_revenues.user_id = %s.user_id';
begin
   return format(query, $1,$1,$1,$1,$1,$1,$1);
end;
$$
language plpgsql;

create or replace function normalize(varchar) returns void as
$$
declare
  query varchar := 'update days_revenues set %s = round(coalesce(%s,0)::numeric,3)';
begin
   execute format(query, $1, $1);
end;
$$
language plpgsql;

create or replace function create_features(low int, up int) returns void as
$$
declare
  name varchar;
begin
  execute 'drop table if exists days_revenues';
  execute 'create temp table days_revenues as select user_id from features';
  for i in low..up loop
    name := concat('day', i);
    begin
      execute format('drop table if exists %s',name);
      execute init_table(name, i-1, i);
      execute create_column(name);
      execute update_column(name);
      execute normalize(name);
    end;
  end loop;
end;
$$
language plpgsql;

select create_features(1,7);
\copy (select days_revenues.*, features.week_revenue, features.month_revenue from features join days_revenues on features.user_id=days_revenues.user_id) to '/tmp/data.csv' with CSV;


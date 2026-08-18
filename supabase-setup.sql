-- Caarangue Yoon — mise en place des comptes & rôles réels avec Supabase
--
-- À exécuter UNE SEULE FOIS dans : Supabase → ton projet → SQL Editor → New query
-- (coller tout ce fichier, puis cliquer "Run").
--
-- Ce script crée :
--   1) une table "profiles" qui stocke le nom, l'email, le rôle et le statut
--      de chaque compte (liée à l'authentification Supabase intégrée) ;
--   2) un déclencheur qui crée automatiquement une ligne "profiles" dès
--      qu'une personne s'inscrit sur le site, avec le rôle par défaut
--      "Agent de terrain" et le statut "En attente" ;
--   3) des règles de sécurité (Row Level Security) : tout compte connecté
--      peut voir la liste des comptes, mais seul un compte Administrateur
--      actif peut modifier le rôle ou le statut d'un autre compte.

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  nom text not null default '',
  email text not null,
  role text not null default 'Agent de terrain'
    check (role in ('Administrateur', 'Superviseur', 'Analyste BAAC', 'Agent de terrain')),
  statut text not null default 'En attente'
    check (statut in ('Actif', 'Inactif', 'En attente')),
  created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;

drop policy if exists "profiles_select_authenticated" on public.profiles;
create policy "profiles_select_authenticated"
  on public.profiles for select
  to authenticated
  using (true);

drop policy if exists "profiles_update_by_admin" on public.profiles;
create policy "profiles_update_by_admin"
  on public.profiles for update
  to authenticated
  using (
    exists (
      select 1 from public.profiles p
      where p.id = auth.uid() and p.role = 'Administrateur' and p.statut = 'Actif'
    )
  );

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, nom, email, role, statut)
  values (new.id, coalesce(new.raw_user_meta_data->>'nom', ''), new.email, 'Agent de terrain', 'En attente');
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ------------------------------------------------------------------------
-- ÉTAPE MANUELLE À FAIRE APRÈS AVOIR EXÉCUTÉ CE SCRIPT :
--
-- 1) Ouvre le site (index.html configuré avec ton URL/clé Supabase) et
--    crée TON PROPRE compte via "Créer un compte".
-- 2) Reviens ici dans le SQL Editor et exécute la ligne suivante en
--    remplaçant l'adresse email par la tienne, pour te promouvoir
--    toi-même Administrateur actif (le seul moment où l'on modifie un
--    rôle "à la main" — après ça, tout se fait depuis la page
--    "Comptes & rôles" du site) :
--
--    update public.profiles set role = 'Administrateur', statut = 'Actif'
--    where email = 'ton-email@exemple.com';
-- ------------------------------------------------------------------------

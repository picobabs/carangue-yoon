-- Caarangue Yoon — table réelle des signalements (accidents)
--
-- À exécuter dans : Supabase → ton projet → SQL Editor → New query
-- (coller tout ce fichier, puis cliquer "Run"). Nécessite que
-- supabase-setup.sql (comptes & rôles) ait déjà été exécuté avant celui-ci,
-- car les règles de sécurité ci-dessous s'appuient sur la table "profiles".
--
-- Ce script crée une table "signalements" qui stocke réellement, de façon
-- partagée entre tous les utilisateurs connectés, les accidents saisis via
-- le formulaire "+ Nouveau signalement" du site. Les photos/croquis/
-- documents ne sont PAS inclus dans cette étape (ils restent, pour
-- l'instant, uniquement dans le navigateur de la personne qui les a
-- ajoutés) — ce sera une étape séparée si besoin.

create table if not exists public.signalements (
  ref text primary key,
  created_by uuid references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),

  statut text not null default 'En attente'
    check (statut in ('En attente', 'En analyse', 'Validé', 'Rejeté')),
  motif_rejet text,

  pv text,
  date_pv date,
  date_accident date,
  heure_accident text,

  region text,
  departement text,
  commune text,
  localite text,
  zone text,
  type_route text,
  numero_route text,
  intersection text,
  type_intersection text,
  moment_jour text,
  eclairage_public text,
  source text,
  lat text,
  lng text,
  adresse text,

  meteo_condition text,
  meteo_temp text,
  meteo_precip text,
  meteo_vent text,
  meteo_visibilite text,
  meteo_etat_route text,

  gravite text,
  cause_presumee text,
  nb_vehicules text,
  transport_commun boolean not null default false,
  transport_commun_type text,
  temoins_presents boolean not null default false,
  temoins_contacts text,
  description text,
  total_personnes text
);

alter table public.signalements enable row level security;

-- Tout compte connecté et actif peut voir tous les signalements.
drop policy if exists "signalements_select_authenticated" on public.signalements;
create policy "signalements_select_authenticated"
  on public.signalements for select
  to authenticated
  using (true);

-- Tout compte connecté peut créer un signalement, à condition de
-- l'enregistrer sous sa propre identité (pas au nom de quelqu'un d'autre).
drop policy if exists "signalements_insert_own" on public.signalements;
create policy "signalements_insert_own"
  on public.signalements for insert
  to authenticated
  with check (created_by = auth.uid());

-- Seuls les rôles Superviseur/Administrateur actifs peuvent modifier un
-- signalement (validation, rejet, correction de statut).
drop policy if exists "signalements_update_by_supervisor" on public.signalements;
create policy "signalements_update_by_supervisor"
  on public.signalements for update
  to authenticated
  using (
    exists (
      select 1 from public.profiles p
      where p.id = auth.uid()
        and p.role in ('Administrateur', 'Superviseur')
        and p.statut = 'Actif'
    )
  );

-- Seul un Administrateur actif peut supprimer définitivement un
-- signalement (même règle que côté interface).
drop policy if exists "signalements_delete_by_admin" on public.signalements;
create policy "signalements_delete_by_admin"
  on public.signalements for delete
  to authenticated
  using (
    exists (
      select 1 from public.profiles p
      where p.id = auth.uid() and p.role = 'Administrateur' and p.statut = 'Actif'
    )
  );

-- Maintient updated_at à jour automatiquement à chaque modification.
create or replace function public.touch_signalement_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists on_signalement_updated on public.signalements;
create trigger on_signalement_updated
  before update on public.signalements
  for each row execute function public.touch_signalement_updated_at();

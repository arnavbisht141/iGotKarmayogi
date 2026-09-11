create table if not exists fields (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  slug text unique not null
);

create table if not exists topics (
  id uuid primary key default gen_random_uuid(),
  field_id uuid references fields(id) on delete cascade,
  name text not null,
  slug text not null,
  unique (field_id, slug)
);

create table if not exists resources (
  id uuid primary key default gen_random_uuid(),
  topic_id uuid references topics(id) on delete cascade,
  type text not null check (type in ('article', 'course')),
  title text not null,
  url text not null,
  provider text,
  thumbnail_url text,
  body_text text,
  description text,
  created_at timestamptz default now(),
  unique (topic_id, url)
);

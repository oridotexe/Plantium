import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm';

const SUPABASE_URL = 'https://hdiokwzwpujvljzcbawz.supabase.co';
const SUPABASE_KEY = 'sb_publishable_JCfuHZKEi34f8zmBpUsAEQ_AIKKM6DL';

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

async function testConnection() {
  console.log("ENTRAAAA");
  const { data, error } = await supabase
    .from('crop')   // nombre de tu tabla
    .select('*')
    .limit(5);

  if (error) {
    console.error('Error conectando a Supabase:', error);
  } else {
    console.log('Datos recibidos:', data);
  }
}

console.log("holaaaa");
testConnection();

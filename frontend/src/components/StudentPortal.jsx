import React, { useState, useEffect } from "react";

export default function StudentPortal({ apiBase = "http://localhost:8000/api/v1" }) {
  const [lang, setLang] = useState("ar");
  const [identifier, setIdentifier] = useState("");
  const [pin, setPin] = useState("");
  const [token, setToken] = useState("");
  const [profile, setProfile] = useState(null);
  const [top10, setTop10] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const isAr = lang === "ar";

  useEffect(() => {
    document.documentElement.dir = isAr ? "rtl" : "ltr";
    document.documentElement.lang = lang;
    fetch(`${apiBase}/public/top-10/`)
      .then((r) => r.json())
      .then((d) => setTop10(d.top_10 || []))
      .catch(() => {});
  }, [lang, apiBase]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await fetch(`${apiBase}/student-portal/login/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ identifier, pin }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || (isAr ? "بيانات الدخول غير صحيحة" : "Invalid credentials"));
      } else {
        setToken(data.access_token);
        const profRes = await fetch(`${apiBase}/student-portal/me/`, {
          headers: { Authorization: `Bearer ${data.access_token}` },
        });
        const profData = await profRes.json();
        setProfile(profData);
      }
    } catch {
      setError(isAr ? "تعذر الاتصال بالخادم" : "Unable to reach server");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="bg-blue-700 text-white px-6 py-4 flex justify-between items-center shadow">
        <div className="font-bold text-xl">SMART GRADES</div>
        <button
          onClick={() => setLang(isAr ? "en" : "ar")}
          className="bg-white text-blue-700 px-3 py-1 rounded text-sm font-semibold"
        >
          {isAr ? "English" : "العربية"}
        </button>
      </header>

      <main className="max-w-5xl mx-auto p-6 space-y-8">
        {!profile ? (
          <form onSubmit={handleLogin} className="bg-white p-6 rounded-xl shadow max-w-md mx-auto space-y-4">
            <h2 className="text-lg font-bold text-blue-800">
              {isAr ? "الاستعلام عن نتيجة الطالب" : "Student Result Lookup"}
            </h2>
            {error && <div className="bg-red-50 text-red-700 p-3 rounded text-sm">{error}</div>}
            <input
              type="text"
              required
              placeholder={isAr ? "كود الطالب أو الرقم التسلسلي" : "Student Code or Serial No."}
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              className="w-full border rounded px-3 py-2"
            />
            <input
              type="password"
              required
              placeholder={isAr ? "الرقم السري (PIN)" : "PIN"}
              value={pin}
              onChange={(e) => setPin(e.target.value)}
              className="w-full border rounded px-3 py-2"
            />
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-700 hover:bg-blue-800 text-white py-2 rounded font-semibold"
            >
              {loading ? (isAr ? "جاري التحقق..." : "Checking...") : (isAr ? "عرض النتيجة" : "View Result")}
            </button>
          </form>
        ) : (
          <section className="bg-white p-6 rounded-xl shadow space-y-6">
            <div className="flex justify-between items-center border-b pb-4">
              <div>
                <h2 className="text-xl font-bold text-blue-900">{profile.student.full_name_ar}</h2>
                <p className="text-sm text-slate-500">
                  {profile.student.student_code} • {profile.student.group} • {profile.student.academic_year}
                </p>
              </div>
              <button
                onClick={() => { setProfile(null); setToken(""); }}
                className="text-sm text-red-600 underline"
              >
                {isAr ? "خروج" : "Logout"}
              </button>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-xs text-slate-500">{isAr ? "النسبة التراكمية" : "Cumulative %"}</div>
                <div className="text-2xl font-bold text-blue-700">{profile.summary.cumulative_percentage}%</div>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-xs text-slate-500">{isAr ? "التقدير" : "Grade"}</div>
                <div className="text-xl font-bold text-blue-800">{profile.summary.grade_label}</div>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-xs text-slate-500">{isAr ? "إجمالي الدرجات" : "Total Score"}</div>
                <div className="text-xl font-bold">{profile.summary.total_score} / {profile.summary.total_max_score}</div>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-xs text-slate-500">{isAr ? "عدد الامتحانات" : "Exams"}</div>
                <div className="text-xl font-bold">{profile.summary.exams_count}</div>
              </div>
            </div>
          </section>
        )}

        <section className="bg-white p-6 rounded-xl shadow">
          <h3 className="text-lg font-bold text-blue-900 mb-4">
            {isAr ? "لوحة شرف العشرة الأوائل (TOP 10)" : "TOP 10 Honor Roll"}
          </h3>
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-blue-50 text-blue-900">
                <th className="p-2 text-start">{isAr ? "المركز" : "Rank"}</th>
                <th className="p-2 text-start">{isAr ? "الطالب" : "Student"}</th>
                <th className="p-2 text-start">{isAr ? "المجموعة" : "Group"}</th>
                <th className="p-2 text-start">{isAr ? "النسبة" : "Percentage"}</th>
              </tr>
            </thead>
            <tbody>
              {top10.map((row, idx) => (
                <tr key={idx} className="border-t">
                  <td className="p-2 font-bold">#{row.rank}</td>
                  <td className="p-2">{row.student_name}</td>
                  <td className="p-2">{row.group}</td>
                  <td className="p-2 font-semibold text-blue-700">{row.cumulative_percentage}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
}

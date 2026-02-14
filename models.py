diff --git a/hospital_metaheuristic/models.py b/hospital_metaheuristic/models.py
new file mode 100644
index 0000000000000000000000000000000000000000..69b8b06883cb277681f98c3b270f37666a7f489d
--- /dev/null
+++ b/hospital_metaheuristic/models.py
@@ -0,0 +1,104 @@
+from __future__ import annotations
+
+from dataclasses import dataclass, field
+from typing import Dict, List, Literal
+
+Role = Literal["nurse", "cleaning"]
+
+
+@dataclass(frozen=True)
+class StaffMember:
+    """Represents employees and their fatigue"""
+
+    id: str
+    role: Role
+    max_weekly_hours: int
+    fatigue_rate_per_hour: float
+    recovery_per_day_off: float
+
+
+@dataclass(frozen=True)
+class ShiftRequirement:
+    """Role coverage per sgift"""
+
+    name: str
+    required_nurses: int
+    required_cleaning: int
+    cleaning_intensity: float = 1.0
+
+
+@dataclass
+class ProblemInstance:
+    """Check int file"""
+
+    planning_days: int
+    shifts_per_day: int
+    shift_hours: int
+    staff: List[StaffMember]
+    requirements: List[ShiftRequirement]
+    monthly_cleaning_incentive_budget: float = 15_000.0
+    max_consecutive_shifts: int = 4
+    objective_weights: Dict[str, float] = field(
+        default_factory=lambda: {
+            "fatigue": 0.45,
+            "coverage": 0.30,
+            "cleaning_delay": 0.15,
+            "incentive_fairness": 0.10,
+        }
+    )
+
+    def role_ids(self, role: Role) -> List[str]:
+        return [member.id for member in self.staff if member.role == role]
+
+    @classmethod
+    def case_study_default(cls) -> "ProblemInstance":
+        """
+        Two shifts each requiring 3 nurses and 3 cleaning staff.
+        """
+        staff: List[StaffMember] = []
+        for i in range(1, 7):
+            staff.append(
+                StaffMember(
+                    id=f"N{i}",
+                    role="nurse",
+                    max_weekly_hours=36,
+                    fatigue_rate_per_hour=1.0,
+                    recovery_per_day_off=3.0,
+                )
+            )
+        for i in range(1, 7):
+            staff.append(
+                StaffMember(
+                    id=f"C{i}",
+                    role="cleaning",
+                    max_weekly_hours=40,
+                    fatigue_rate_per_hour=1.2,
+                    recovery_per_day_off=2.5,
+                )
+            )
+
+        requirements = [
+            ShiftRequirement(
+                name="day",
+                required_nurses=3,
+                required_cleaning=3,
+                cleaning_intensity=1.2,
+            ),
+            ShiftRequirement(
+                name="night",
+                required_nurses=3,
+                required_cleaning=3,
+                cleaning_intensity=1.0,
+            ),
+        ]
+
+        return cls(
+            planning_days=30,
+            shifts_per_day=2,
+            shift_hours=8,
+            staff=staff,
+            requirements=requirements,
+            monthly_cleaning_incentive_budget=15_000.0,
+            max_consecutive_shifts=4,
+        )

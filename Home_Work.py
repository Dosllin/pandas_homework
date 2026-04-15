import pandas as pd
class AdvancedStudentAnalytics:
    def __init__(self, df):
        self.df = df
        self._prepare_data()
        print(self._valide_col())
        print(all(self.df[col].dtype == 'float64' for col in ['project_score', 'average_grade']))
        if not self._valide_col():
            raise ValueError("DataFrame columns have incorrect types")
    def _prepare_data(self):
        self.df['project_score'] = self.df[['math', 'physics', 'cs']].median(axis=1)
        self.df['average_grade'] = self.df[['math', 'physics', 'cs']].mean(axis=1)
        self.df['performance_level'] = self.df['project_score'].apply(lambda x: 'high' if x >= 85 else ('medium' if x >= 70 else 'low'))
        self.df['risk_level'] = self.df.apply(lambda x: 'high risk' if x['attendance'] < 60 or x['average_grade']<65 else ('medium risk' if x['attendance'] <= 75 else 'low risk'),axis=1)

    def top_students(self,n):
        return self.df.sort_values(by='average_grade', ascending=False).head(n)

    def group_stats(self):
        return self.df.groupby('group').agg({'average_grade': 'mean', 'attendance': 'mean', 'name': 'count'})

    def at_risk_students(self):
        return self.df.query('risk_level == "high risk"')

    def scholarship_analysis(self):
        return self.df.groupby('scholarship').agg({'average_grade': 'mean', 'attendance': 'mean'})

    def city_performance(self):
        return (self.df.sort_values(by='average_grade', ascending=False)['city']).iloc[[0,-1]]

    def hidden_top_students(self):
        return self.df.query('average_grade > 85 and scholarship == False')

    def lazy_geniuses(self):
        return self.df.query('average_grade > 85 and attendance < 60')

    def full_analysis(self):
        dict_result = {
            'top_3': self.top_students(3),
            'group_stats': self.group_stats(),
            'count_risk_students': len(self.at_risk_students()),
            'hidden_top_students': len(self.hidden_top_students()),
            'lazy_geniuses': len(self.lazy_geniuses()),
            'city_performance': self.city_performance(),
            'scholarship_analysis': self.scholarship_analysis(),
        }
        return dict_result

    def performance_distribution(self):
        group = self.df.groupby('performance_level').agg({'name': 'count'})
        group['name'] = (group['name']/group['name'].sum())*100
        return group

    def _valide_col(self):
        if self.df['scholarship'].dtypes == 'bool' and all(self.df[col].dtype == 'str' for col in ['name', 'group', 'city', 'performance_level', 'risk_level']) and \
            all(self.df[col].dtype == 'int64' for col in ['math', 'physics', 'cs', 'attendance']) and all(self.df[col].dtype == 'float64' for col in ['project_score', 'average_grade']):
            print(1)
            return True
        else:
            return False


df = pd.read_csv('students_extended.csv')
# df['math'] = pd.to_numeric(df['math'], errors='coerce', downcast='integer')
analytics = AdvancedStudentAnalytics(df)
analytics.top_students(3)
analytics.group_stats()
# print(analytics.full_analysis())
# print(analytics.performance_distribution())



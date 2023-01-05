# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
import os
import psycopg2
from flask_wtf.csrf import CSRFProtect
from wtforms.validators import DataRequired, NumberRange, Email

class MyForm(FlaskForm):
    Gender = SelectField(u'你的性別', choices=[('男','男'),('女','女')])
    Age = IntegerField(u'你的年齡',validators=[DataRequired(), NumberRange(min=0, max=100, message='')])
    Area = SelectField(u'你來自的地區', choices=[('北部','北部'),('中部','中部'),('南部','南部'),('東部','東部'),('離島','離島'),('外國人','外國人')])
    School = StringField(u'你的學校，請輸入全名',validators=[DataRequired()])
    Study_group = SelectField(u'你的類組', choices=[('文法商','文法商'),('理工','理工'),('生醫農','生醫農'),('其它','其它')])
    Star_sign = SelectField(u'你的星座', choices=[('白羊座','白羊座'),('金牛座','金牛座'),('雙子座','雙子座'),('巨蟹座','巨蟹座'),('獅子座','獅子座'),('處女座','處女座'),('天秤座','天秤座'),('天蠍座','天蠍座'),('射手座','射手座'),('摩羯座','摩羯座'),('水瓶座','水瓶座'),('雙魚座','雙魚座')])
    Q1 = SelectField(u'Q1 : 我樂於"參加聚會"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q2 = SelectField(u'Q2 : 我喜歡探討"未知的知識"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q3 = SelectField(u'Q3 : 我善於闡述"我的感受"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q4 = SelectField(u'Q4 : 我喜歡"按照計劃"行事', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q5 = SelectField(u'Q5 : 我偏好"安靜的場域"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q6 = SelectField(u'Q6 : 我喜歡到"未曾去過"的地方旅行', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q7 = SelectField(u'Q7 : 我看待世界"重視邏輯"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q8 = SelectField(u'Q8 : 我的生活環境"整潔"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q9 = SelectField(u'Q9 : 我喜歡交"很多朋友"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q10 = SelectField(u'Q10 : 我對這個世界"充滿好奇" "', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q11 = SelectField(u'Q11 : 我能感受到環境，及人們"細微的變化"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q12 = SelectField(u'Q12 : 我是個"準時"的人', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q13 = SelectField(u'Q13 : 我更喜歡"獨處"的時間', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q14 = SelectField(u'Q14 : 我忠於"傳統"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q15 = SelectField(u'Q15 : 我"避免爭執"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    Q16 = SelectField(u'Q16 : 我的行為模式"易於預測"', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    submit = SubmitField('Submit')

'''
Service Initialization.
'''
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = os.urandom(24)
csrf = CSRFProtect(app)
'''
Connect to database.
'''
rds_host = "RDS database endpoints"
rds_port = 5432
rds_user = "postgres"
rds_password = "password"
rds_database = "data"

conn = psycopg2.connect(
    host=rds_host,
    port=rds_port,
    user=rds_user,
    password=rds_password,
    database=rds_database
)

db_engine = conn.cursor()


'''
Function to get form data.
'''
def get_data(form):
    '''
    get data
    '''
    gender = form.Gender.data
    age = form.Age.data
    area = form.Area.data
    school = form.School.data
    study_group = form.Study_group.data
    star_sign = form.Star_sign.data
    q1 = int(form.Q1.data)
    q2 = int(form.Q2.data)
    q3 = int(form.Q3.data)
    q4 = int(form.Q4.data)
    q5 = int(form.Q5.data)
    q6 = int(form.Q6.data)
    q7 = int(form.Q7.data)
    q8 = int(form.Q8.data)
    q9 = int(form.Q9.data)
    q10 = int(form.Q10.data)
    q11 = int(form.Q11.data)
    q12 = int(form.Q12.data)
    q13 = int(form.Q13.data)
    q14 = int(form.Q14.data)
    q15 = int(form.Q15.data)
    q16 = int(form.Q16.data)

    mind = -(q1-3)+(q5-3)-(q9-3)+(q13-3)
    energy = (q2-3)+(q6-3)+(q10-3)-(q14-3)
    nature = (q3-3)-(q7-3)+(q11-3)+(q15-3)
    tactics = -(q4-3)-(q8-3)-(q12-3)-(q16-3)

    mbti = ('E' if mind<=0 else 'I') + ('S' if energy<=0 else 'N') + ('T' if nature<=0 else 'F') + ('J' if tactics<=0 else 'P')
    
    '''
    Database update
    '''
    db_engine.execute("""
        select max(index) from test_result;
    """)
    index = list(db_engine.fetchall())[0][0] + 1
    db_engine.execute(f"""
        insert into subject(index, gender, age)
        VALUES ({index},'{gender}','{age}');"""
    )
    db_engine.execute(f"""
        insert into test_result(index, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11,
                                q12, q13, q14, q15, q16, mbti_result)
        VALUES ({index}, {q1}, {q2}, {q3}, {q4}, {q5}, {q6}, {q7}, {q8}, {q9}, {q10}, {q11}, {q12}, {q13},
                        {q14}, {q15}, {q16}, '{mbti}');
    """)
    db_engine.execute(f"""
        insert into study(index, school_name, study_group)
        VALUES ({index}, '{school}', '{study_group}');
    """)
    db_engine.execute(f"""
        insert into subject_star_sign(index, star_sign)
        VALUES ({index}, '{star_sign}');
    """)
    db_engine.execute(f"""
        insert into hometown(index, area)
        VALUES ({index}, '{area}');
    """)
    db_engine.execute("COMMIT")
    return mbti, gender, age

@app.route('/',methods=['GET', 'POST'])
def index():
    mbti_statement = {
        'INTJ' :  ('建筑师','富有想象力和战略性的思想家，一切皆在计划之中。'),
        'INTP' :  ('逻辑学家','具有创造力的发明家，对知识有着止不住的渴望。'),
        'ENTJ' :  ('指挥官','大胆，富有想象力'),
        'ENTP' :  ('辩论家','聪明好奇的思想者，不会放弃任何智力上的挑战。'),

        'INFJ' :  ('提倡者','安静而神秘，同时鼓舞人心且不知疲倦的理想主义者。'),
        'INFP' :  ('调停者','诗意，善良的利他主义者，总是热情地为正当理由提供帮助。'),
        'ENFJ' :  ('主人公','富有魅力鼓舞人心的领导者，有使听众着迷的能力。'),
        'ENFP' :  ('竞选者' '热情，有创造力爱社交的自由自在的人，总能找到理由微笑。'),

        'ISTJ' :  ('物流师','实际且注重事实的个人，可靠性不容怀疑。'),
        'ISFJ' :  ('守卫者','非常专注而温暖的守护者，时刻准备着保护爱着的人们。'),
        'ESTJ' :  ('总经理','出色的管理者，在管理事情或人的方面无与伦比。'),
        'ESFJ' :  ('执政官','极有同情心，爱交往受欢迎的人们，总是热心提供帮助。'),

        'ISTP' :  ('鉴赏家','大胆而实际的实验家，擅长使用任何形式的工具。'),
        'ISFP' :  ('探险家','灵活有魅力的艺术家，时刻准备着探索和体验新鲜事物。'),
        'ESTP' :  ('企业家','聪明，精力充沛善于感知的人们，真心享受生活在边缘。'),
        'ESFP' :  ('表演者','自发的，精力充沛而热情的表演者－生活在他们周围永不无聊。')
    }
    form = MyForm()
    if request.method == 'POST' and form.validate():
        '''
        mbti match query
        '''
        mbti, gender, age = get_data(form)

        if gender == '男':
            gender = '女'
        else:
            gender = '男'
        '''
        check update
        '''
        '''
        db_engine.execute(f"""
            select * from hometown;
        """)
        datas = list(db_engine.fetchall())
        test = ""
        for data in datas:
            for i in data:
                test += str(i)
            test += "<br>"
        '''
        db_engine.execute(f"""
            create or replace view matched_mbti as
            (
                select suitable_mbti
                from mbti_match
                where asked_mbti = '{mbti}'
            );
            
            create or replace view matched_index as
            (
                select index, matched_mbti
                from subject natural join test_result, matched_mbti
                where 
                age between '{age}' - 2 and '{age}' + 2 and 
                gender = '{gender}' and mbti_result = suitable_mbti
            );


            select 
                cast(count(index) as float) * 100 / (select count(index) from subject) 
                        as percentage
            from matched_index;
        """)
        
        datas = list(db_engine.fetchall())
        str1 = ""
        for data in datas:
            for i in data:
                str1 += str(i)
            str1 += "% "
        str1 = "在曾經參與此網站檢測的人當中，與你適配的異性有 : " + str1 + "<br>"
        db_engine.execute(f"""
            
            select area,
	            cast(count(area) as float) * 100 / 
		        (select count(index) from matched_index natural join hometown) as percentage
            from matched_index natural join hometown 
            group by area
            order by percentage desc;
        """)
        datas = list(db_engine.fetchall())
        str2 = ""
        for data in datas:
            for i in data:
                str2 += str(i)
            str2 += "% "
        str2 = "配對對象的地區分布 : " + str2 + "<br>"
        db_engine.execute(f"""
            select 
	            star_sign,
                cast(count(star_sign) as float) * 100 / 
                (select count(index) from matched_index natural join subject_star_sign)
                    as percentage
            from matched_index natural join subject_star_sign
            group by star_sign
            order by percentage desc
        """)
        datas = list(db_engine.fetchall())
        str3 = ""
        for data in datas:
            for i in data:
                str3 += str(i)
            str3 += "% "
        str3 = "配對對象的星座分布 : " + str3 + "<br>"
        db_engine.execute(f"""
            select 
                school_name,
                cast(count(school_name) as float) * 100 / 
                    (select count(index) from matched_index natural join study)
                    as percentage
            from matched_index natural join study
            group by school_name
            order by percentage desc
        """)
        datas = list(db_engine.fetchall())
        str4 = ""
        for data in datas:
            for i in data:
                str4 += str(i)
            str4 += "% "
        str4 = "配對對象的學校分布 : " + str4 + "<br>"
        return "你的性格是 : " + mbti + "<br>" + mbti_statement[mbti][0] + " : " + mbti_statement[mbti][1] + "<br>" + str1 + str2 + str3 + str4

    return render_template('layout.html',form=form)

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)
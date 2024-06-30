from app.main import create_app, db
from app.models.models import User, Event

def main():
    app = create_app()
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 检查是否已存在用户
        existing_user = User.query.filter_by(name="张大爷").first()
        if not existing_user:
            # 创建一个示例用户
            user = User(name="张大爷", age=70)
            db.session.add(user)
            db.session.commit()
            print("已添加示例用户：张大爷")
        else:
            print("示例用户已存在，跳过创建")

        print("数据库初始化完成。")

if __name__ == "__main__":
    main()
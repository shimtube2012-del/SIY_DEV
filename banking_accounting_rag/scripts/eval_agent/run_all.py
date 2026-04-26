"""전체 평가 파이프라인 순차 실행."""
import eval_config  # sys.path 세팅

import step1_generate_qa
import step2_run_rag
import step3_judge
import step4_report


def main():
    step1_generate_qa.main()
    step2_run_rag.main()
    step3_judge.main()
    step4_report.main()


if __name__ == "__main__":
    main()

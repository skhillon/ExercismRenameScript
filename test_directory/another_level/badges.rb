FactoryBot.define do
  factory :badge, class: 'Badges::RookieBadge' do
    user { create :user }
  end
end
